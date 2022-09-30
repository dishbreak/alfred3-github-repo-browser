package main

import "github.com/alecthomas/kong"

type Context struct{}
type Cli struct{}

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
