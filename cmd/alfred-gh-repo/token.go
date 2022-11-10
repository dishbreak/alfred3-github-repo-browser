package main

import (
	"bufio"
	"context"
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strings"

	"github.com/dishbreak/go-alfred/alfred"
	"github.com/google/go-github/v47/github"
	"github.com/zalando/go-keyring"
	"golang.org/x/oauth2"
)

type SetTokenCmd struct{}

func (t *SetTokenCmd) Help() string {
	return `
Saves a token to the keychain. Note that tokens must be passed in via stdin.
	`
}

const (
	tokenName = "github-access-token"
)

func (t *SetTokenCmd) Run(c *Context) error {
	var token string
	resp := alfred.NewScriptActionResponse()

	defer alfred.RecoverIfErr(resp)()

	if stat, _ := os.Stdin.Stat(); (stat.Mode() & os.ModeCharDevice) == 0 {
		b, err := ioutil.ReadAll(os.Stdin)
		if err != nil {
			panic(err)
		}
		token = string(b)
	} else {
		fmt.Println("Enter Github Token, press enter when done.")
		reader := bufio.NewReader(os.Stdin)
		token, _ = reader.ReadString('\n')
	}

	token = strings.TrimSpace(token)

	if len(token) == 0 {
		panic(errors.New("cowardly refusing to set an empty token"))
	}

	if err := keyring.Set(appName, tokenName, token); err != nil {
		panic(err)
	}

	resp.SetVariable(alfred.ExecStatus, alfred.StatusOk)
	resp.SendFeedback()
	return nil
}

func getGithubClient(ctx context.Context) (*github.Client, error) {
	token, err := keyring.Get(appName, tokenName)
	if err != nil {
		return nil, err
	}

	src := oauth2.StaticTokenSource(
		&oauth2.Token{
			AccessToken: token,
		},
	)

	httpClient := oauth2.NewClient(ctx, src)
	if err != nil {
		return nil, err
	}

	ghClient := github.NewClient(httpClient)
	return ghClient, nil
}

type DeleteTokenCmd struct{}

func (d *DeleteTokenCmd) Help() string {
	return `
Deletes the stored Github token from the keyring.	
	`
}

func (d *DeleteTokenCmd) Run(c *Context) error {
	resp := alfred.NewScriptActionResponse()
	defer alfred.RecoverIfErr(resp)()

	if err := keyring.Delete(appName, tokenName); err != nil {
		panic(err)
	}

	resp.SendFeedback()
	return nil
}
