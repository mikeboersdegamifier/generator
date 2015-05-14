# GitHub Degameifier Generator

This `generate.py` script creates a git repo that will create a pattern in your GitHub contribution activity.

It parses the HTML of your public profile to determine how much activity you already have for any given day, so that actual activity does not disrupt the pattern. This only works if the degameifier did not already run for the requested date range.

[Read the blog post for why.][blog]

~~~
# Generate new content:
python generate.py \
    --name 'Mike Boers' \
    --email 'github@mikeboers.com' \
    --start 2015-01-01 \
    --end 2015-04-30 \
    --refresh \
    --init \
    --max 44 \
    mikeboers

~~~

[blog]: http://mikeboers.com/blog/2014/10/26/the-evils-of-gamifying-git
