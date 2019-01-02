# Alfred Github Repo Browser

Review and open Github repos from the comfort of Alfred 3.

![Sample Repos](/img/launcher.png)

Made possible by Dean Jackson's awesome [alfred-workflow](https://github.com/deanishe/alfred-workflow/) package.

# Installation

Download the most recent release from the Releases tab.

# Usage

## Configure
Before you can use the workflow the workflow, you'll want to configure an API key. Use the keyword `ghsettings` in Alfred 3 to bring it up.

![Github Settings](/img/settings.png)

Once that's done, you can use the `ghrepo` keyword to jump to a Github Repo!

## Go to Github Repo
Use the keyword `ghrepo <REPO_NANE>` to jump to your favorite Github Repo!
..._(note if you have a lot of repos and this is your first time the auto complete won't work, just give it a bit and you will bask in all its glory)._

In most cases you want to go to the homepage so just hit a double enter when choosing your repo to go there.

But wait there's more... If you want to go to a specific page within the repo, after you select the github repo, we ask where you want to go in the repo.

![Github Repo Pages](/img/repo_pages.png)


## Go to my Github Pulls
Use the keyword `ghpulls` to jump to your open pull requests. Like the `ghrepo` command if you just want to go to the pulls homepage double hit enter.

But wait there's more... again... If you want to go to a specific page like pull requests assigned or mentioned, we ask you that as well.

# Caching

If you've got a lot of repos on Github, it can take awhile for the plugin to retrieve them all. To help with that, the plugin will cache results for an hour by default.

You can change the cache timeout or clear the cache from the settings menu.

# Contributing
## Editing the Source Code
TODO: fill this out

## Editing the Workflow
If you want to edit something like adding a new keyword command you are going to have to edit the Alfred workflow itself via the GUI. But once you're done you want to retrieve your live edits and commit them back to this repo.

The Workflow information is stored in a special file called 'info.plist'. You can see the current workflow in `./info.plist`. But the live workflow is buried under a random hash in your application support directory.

Run `update_plist.sh` to find the current running `plist.info` file and override the local `./plist.info` file and commit that to this repo.
