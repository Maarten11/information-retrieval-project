<script lang="ts">
	export interface IRecipe {
		Images?: string;
		Name: string;
		RecipeIngredientParts: Array<string>;
		RecipeInstructions: Array<string>;
		Rating?: string;
	}
</script>
<script setup lang="ts">
	import imgUrl from "../assets/recipe_placeholder.jpg";
	const props = defineProps<IRecipe>();

	const ratingInt: undefined | number = !!props.Rating
		? Math.floor(Number.parseFloat(props.Rating))
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
				<span v-if="ratingInt != undefined" class="block text-sm"
					>{{ ratingInt }}/5</span
				>
			</div>
			<!-- <ul>
				<li
					v-for="(ingredient, index) in props.RecipeIngredientParts"
					:key="index">
					{{ ingredient }}
				</li>
			</ul> -->
			<span class="text-sm">{{ props.RecipeIngredientParts.join(", ") }}</span>
		</div>
	</div>
</template>
