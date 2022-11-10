package main

import (
	"context"

	"github.com/dishbreak/go-alfred/alfred"
	"github.com/google/go-github/v47/github"
)

type ListReposCommand struct{}

func (l *ListReposCommand) Help() string {
	return `
	Lists all matching Github Repos. Note that archived repos will appear in the list.
	`
}

const (
	repoCache = "github_repos"
)

func getRepoCache(ctx context.Context) (*alfred.ItemCache, error) {
	timeout, err := GetCacheTimeout()
	if err != nil {
		return nil, err
	}
	ghClient, err := getGithubClient(ctx)
	if err != nil {
		panic(err)
	}

	return alfred.NewCache(repoCache, timeout, func() ([]alfred.ListItem, error) {
		opts := &github.RepositoryListOptions{}

		items := make([]alfred.ListItem, 0)
		for {
			repos, resp, err := ghClient.Repositories.List(ctx, "", opts)
			if err != nil {
				return items, err
			}
			for _, repo := range repos {
				item := alfred.ListItem{
					Title: *repo.FullName,
					Arg:   *repo.HTMLURL,
					Valid: true,
				}
				if repo.Description != nil {
					item.Subtitle = *repo.Description
				}
				items = append(items, item)
			}
			if resp.NextPage == 0 {
				break
			}
			opts.Page = resp.NextPage
		}
		return items, nil
	})
}

func (l *ListReposCommand) Run() error {
	resp := alfred.NewScriptFilterResponse()

	defer alfred.RecoverIfErr(resp)()

	ctx := context.Background()

	cache, err := getRepoCache(ctx)
	if err != nil {
		panic(err)
	}

	items, err := cache.Get()
	if err != nil {
		panic(err)
	}
	for _, item := range items {
		resp.AddItem(item)
	}

	resp.SendFeedback()
	return nil
}

type FlushCacheCommand struct{}

func (f *FlushCacheCommand) Help() string {
	return `
	Refreshes the repo cache with new data from the Github API.
	`
}

func (f *FlushCacheCommand) Run() error {
	resp := alfred.NewScriptActionResponse()
	defer alfred.RecoverIfErr(resp)()

	ctx := context.Background()

	cache, err := getRepoCache(ctx)
	if err != nil {
		panic(err)

	}

	err = cache.Flush()
	if err != nil {
		panic(err)
	}

	return nil
}
