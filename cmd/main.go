package main

import "github.com/alecthomas/kong"

type Context struct{}
type Cli struct {
	SetToken    SetTokenCmd    `cmd:"set-token" help:"Set a GitHub Access Token"`
	DeleteToken DeleteTokenCmd `cmd:"delete-token" help:"Erase the configured GitHub Access Token"`
}

const (
	appName = "gh-browser"
	appDesc = "A CLI tool for fetching Github data for Alfred"
)

func main() {
	cli := &Cli{}
	ctx := kong.Parse(cli, kong.Name(appName), kong.Description(appDesc))
	err := ctx.Run(&Context{})
	ctx.FatalIfErrorf(err)
}
