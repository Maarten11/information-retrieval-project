# Project Data

Here follows some explanation around the used data and how to set it up for the project.

## Setup

The _Food.com_ dataset is too large to include in the repository.
It will have to be downloaded manually.
The parquet files of the dataset should be put inside of this directory.

## Data structure

The expected columns of a used dataset are given below.
Any additional dataset should thus have at least these columns.
Additional columns will be ignored.

| **Name**              | **Type**               |
| --------------------- | ---------------------- |
| **_Recipe files_**    |                        |
| Name                  | _string_               |
| RecipeId              | _int_                  |
| RecipeIngredientParts | _list: string_         |
| RecipeInstructions    | _list: string_         |
| Images                | _list: string_         |
| CookTime              | _string(iso duration)_ |
| **_Review files_**    |                        |
| RecipeId              | _int(maps to Recipes)_ |
| Rating                | _float \| int_         |

## Datasets

For the project we used following datasets:

| **Dataset**                    | **Source**                                                                   | **Present** |
| ------------------------------ | ---------------------------------------------------------------------------- | ----------- |
| Food.com - Recipes and Reviews | [Kaggle](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews) | :x:         |
