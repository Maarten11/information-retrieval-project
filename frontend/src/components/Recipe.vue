<script lang="ts">
	export interface IRecipe {
		Images?: string;
		Name: string;
		RecipeIngredientParts: Array<string>;
		RecipeInstructions: Array<string>;
	}
</script>
<script setup lang="ts">
	import imgUrl from "../assets/recipe_placeholder.jpg";
	const props = defineProps<IRecipe>();
</script>

<template>
	<div
		class="shadow-lg bg-stone-800 bg-opacity-35 overflow-hidden rounded-md grid grid-cols-[auto,1fr] gap-5">
		<img
			class="aspect-square max-h-24 object-cover overflow-hidden"
			:src="props.Images ?? imgUrl"
			:alt="Name" />
		<div class="grid grid-flow-row text-left">
			<h3 class="text-md">{{ props.Name }}</h3>
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
