# Project Data

Here follows some explenation around the used data and how to set it up for the project.

## Setup

The _Food.com_ dataset is too large to include in the repository.
It will have to be downloaded manually.
The parquet files of the dataset should be put inside of this directory.

## Data structure

The expected columns of a used dataset are given below.
Any additional dataset should thus have at least these columns.
Additional columns will be ignored.

| **Name**              | **Type**       |
| --------------------- | -------------- |
| Name                  | _string_       |
| RecipeId              | _int_          |
| RecipeIngredientParts | _list: string_ |
| RecipeInstructions    | _list: string_ |
| Images                | _list: string_ |
| CookTime              | _datetime_     |

## Datasets

For the project we used following datasets:

| **Dataset**                    | **Source**                                                                   | **Present** |
| ------------------------------ | ---------------------------------------------------------------------------- | ----------- |
| Food.com - Recipes and Reviews | [Kaggle](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews) | :x:         |
