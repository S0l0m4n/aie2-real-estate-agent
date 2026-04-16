Feature value decoding
======================
### MSSubClass
The `MSSubClass` value has these meanings:
```
20: 1-STORY 1946 & NEWER ALL STYLES
30: 1-STORY 1945 & OLDER
40: 1-STORY W/FINISHED ATTIC ALL AGES
45: 1-1/2 STORY - UNFINISHED SECOND LEVEL
50: 1-1/2 STORY FINISHED ALL AGES
60: 2-STORY 1946 & NEWER
70: 2-STORY 1945 & OLDER
75: 2-1/2 STORY ALL AGES
80: SPLIT OR MULTI-LEVEL
85: SPLIT FOYER
90: DUPLEX - ALL STYLES AND AGES
120: 1-STORY PUD (PLANNED UNIT DEVELOPMENT) - 1946 & NEWER
150: 1-1/2 STORY PUD - ALL AGES
160: 2-STORY PUD - 1946 & NEWER
180: PUD - MULTILEVEL - INCL SPLIT FOYER
190: 2 FAMILY CONVERSION - ALL STYLES AND AGES 
```

The most common values are:
* 20	(323)   -   1-story, post 1946
* 60	(174)   -   2-story, post 1946
* 50	(86)    -   1.5 story
* 120   (52)    -   1-story, new development
* 160	(43)    -   2-story, new development
* 30	(40)    -   1-story, pre 1946
* 70	(39)    -   2-story, pre 1945
* 80	(33)    -   multi-level
* 90	(29)    -   duplex

The most reasonable things to ask a user is:
* how many stories (1, 1.5, 2+)
    - 2+ (75) is absorbedi into 2 
* house age (relates to `YearBuilt` feature)
    - classify as pre/post 1946 based on stories value
* if user mentions new development, classiy as 120/160 accordingly
* if multi-level/duplex is mentioned, classify as 80/90 accordingly
* other = 190

**Rationale:**
Unhandled categories:
* 190, 85, 45, 180, 40

Looking at the mean sale price value for these categories, they range from $100 - $150k, with the most common value being 190 with a mean sale price in the middle, around $130k. So we use 190 for "other" or unknown homes.

### OverallQual
Check out the histogram like this:
`df['OverallQual'].hist(bins=10)`

Value is between 1-10. Most values are between 4 - 8. Property value increases markedly for 8+. Ask the user to rate the overall quality between 1 - 10.

Otherwise, if they describe the house with adjectives, map as follows:
* fair or below average => 4
* good or average       => 6
* great or better       => 8

### YearBuilt, YearRemodAdd
Here we graph the two together by binning them:
```
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

df['YearBuilt_bin'] = pd.cut(df['YearBuilt'], bins=16)
bin_means_0 = df.groupby('YearBuilt_bin')['SalePrice'].mean()
axes[0].bar(range(len(bin_means_0)), bin_means_0.values)
axes[0].set_xticks(range(len(bin_means_0)))
axes[0].set_xticklabels([str(int(b.left)) for b in bin_means_0.index], rotation=45, ha='right')
axes[0].set_xlabel('YearBuilt')
axes[0].set_ylabel('Mean SalePrice')
axes[0].set_title('Sale Price vs Year Built')

df['YearRemodAdd_bin'] = pd.cut(df['YearRemodAdd'], bins=6)
bin_means_1 = df.groupby('YearRemodAdd_bin')['SalePrice'].mean()
axes[1].bar(range(len(bin_means_1)), bin_means_1.values)
axes[1].set_xticks(range(len(bin_means_1)))
axes[1].set_xticklabels([str(int(b.left)) for b in bin_means_1.index], rotation=45, ha='right')
axes[1].set_xlabel('YearRemodAdd')
axes[1].set_ylabel('Mean SalePrice')
axes[1].set_title('Sale Price vs Year Remodelled')

plt.tight_layout()
plt.show()
```
YearBuilt is always relevant, a house is only remodelled if YearRemodAdd has a different (later) value. If the house is not remodelled, then it's set to the same value as YearBuilt. I'm going to rerun the training model with this feature removed and see if it performs better. If it's not much different, we'll remove it.

### Neighborhood
The values for `Neighborhood` are:
...
