<script lang="ts">
	export interface IRecipe {
		Images?: string;
		Name: string;
		RecipeIngredientParts: Array<string>;
		RecipeInstructions: Array<string>;
		Rating?: string;
		CookTime?: string;
	}
</script>
<script setup lang="ts">
	import imgUrl from "../assets/recipe_placeholder.jpg";
	const props = defineProps<IRecipe>();

	const ratingInt: undefined | number = !!props.Rating
		? Math.floor(Number.parseFloat(props.Rating))
		: undefined;

	const cookTime: undefined | string = !!props.CookTime
		? new Date(Number.parseInt(props.CookTime) * 1000)
				.toISOString()
				.split("T")[1]
				.substring(0, 5)
				.replace(":", "h ")
				.concat("m")
		: undefined;
</script>

<template>
	<div
		class="shadow-xl bg-stone-800 bg-opacity-35 overflow-hidden rounded-md grid grid-cols-[auto,1fr] gap-5 pe-5">
		<img
			class="aspect-square max-h-24 object-cover overflow-hidden"
			:src="props.Images ?? imgUrl"
			:alt="Name" />
		<div class="grid grid-flow-row text-left py-2">
			<div class="flex justify-between">
				<h3 class="text-md">{{ props.Name }}</h3>
				<div class="grid min-w-[7ch]">
					<span v-if="ratingInt != undefined" class="block text-sm">
						{{ ratingInt }}/5
					</span>
					<span v-if="cookTime != undefined" class="block text-sm">
						{{ cookTime }}
					</span>
				</div>
			</div>
			<span class="text-sm">{{ props.RecipeIngredientParts.join(", ") }}</span>
		</div>
	</div>
</template>
