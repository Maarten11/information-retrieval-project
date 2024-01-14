<script setup lang="ts">
	import { Ref, ref } from "vue";
	import Recipe, { IRecipe } from "./components/Recipe.vue";
	import imgUrl from "./assets/recipe_placeholder.jpg";

	const elements: Ref<IRecipe[] | null> = ref(null);
	const search = async () => {
		const form = new FormData();
		form.append("include", JSON.stringify(["apple"]));
		const request = await fetch("http://localhost:8000/search_recipe", {
			body: form,
			method: "POST",
		});
		const response = await request.json();
		elements.value = response;
	};
	const selectedRecipe: Ref<IRecipe | undefined> = ref(undefined);
	const select = (recipe: IRecipe | undefined) => {
		console.log("Selecting");
		selectedRecipe.value = recipe;
	};
</script>

<template>
	<h1 class="text-3xl">Recipe Searcher</h1>
	<button @click="search">Search</button>
	<div class="grid gap-5">
		<Recipe
			class="hover:cursor-pointer"
			@click="select(recipe)"
			v-bind="recipe"
			v-for="(recipe, index) in elements"
			:key="index" />
	</div>
	<div
		v-show="!!selectedRecipe"
		class="fixed m-auto top-0 left-0 h-full w-full p-20 backdrop-blur-md">
		<div class="relative h-full">
			<div
				class="grid grid-rows-[auto,1fr] shadow-lg bg-stone-800 h-full overflow-y-auto rounded-2xl">
				<img
					class="w-full h-[30vh] object-cover"
					:src="selectedRecipe?.Images ?? imgUrl" />
				<button class="absolute top-0 left-0" @click="select(undefined)">
					x
				</button>
				<div class="grid p-10 grid-rows-[auto,1fr] gap-10">
					<h2 class="text-3xl">{{ selectedRecipe?.Name }}</h2>
					<div class="grid grid-flow-col gap-5">
						<aside>
							<h4 class="text-xl">Ingredients:</h4>
							<ul class="text-left">
								<li
									v-for="ingredient in selectedRecipe?.RecipeIngredientParts"
									:key="ingredient">
									{{ ingredient }}
								</li>
							</ul>
						</aside>
						<section class="text-left">
							<h4 class="text-xl">Instructions:</h4>
							<ol>
								<li v-for="instr in selectedRecipe?.RecipeInstructions">
									{{ instr }}
								</li>
							</ol>
						</section>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<style scoped></style>
