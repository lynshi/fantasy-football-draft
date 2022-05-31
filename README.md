# fantasy-football-draft

Python scripts for randomizing a draft order for fantasy football leagues.

# Supported Platforms
- Sleeper

# FAQs
## Why is Sleeper supported when it already has an option to randomize the draft order?
Because some leaguemates requested the ability to set additional rules on the generated draft order.

## Why can the draft order be re-rolled?
If `--num-rolls` is a value greater than 1, the draft order is rolled multiple times (up to the specified amount) and intermediate results are discarded. This is also implemented per league request; per tradition, the draft order is rolled thrice.
