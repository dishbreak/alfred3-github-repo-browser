package main

import (
	"github.com/dishbreak/go-alfred/alfred"
)

type SetTimeoutCmd struct {
	CacheTimeoutInSeconds int `arg:""`
}

func (s *SetTimeoutCmd) Help() string {
	return `
Sets the cache timeout value in seconds. The workflow will retain API data for the configured time interval.
	`
}

func (s *SetTimeoutCmd) Run(c *Context) error {
	resp := alfred.NewScriptActionResponse()

	defer alfred.RecoverIfErr(resp)()

	if err := SetCacheTimeout(s.CacheTimeoutInSeconds); err != nil {
		panic(err)
	}

	resp.SendFeedback()
	return nil
}
