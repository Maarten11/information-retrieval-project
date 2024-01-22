<script setup lang="ts">
	import { Ref, computed, ref } from "vue";
	import Recipe, { IRecipe } from "./components/Recipe.vue";
	import imgUrl from "./assets/recipe_placeholder.jpg";

	const recipes: Ref<IRecipe[] | null> = ref(null);

	const selectedRecipe: Ref<IRecipe | undefined> = ref(undefined);
	const select = (recipe: IRecipe | undefined) => {
		selectedRecipe.value = recipe;
	};

	const searchRecipes = async () => {
		const includeList = !!include.value.length
			? include.value.split(",").map((s) => s.trim())
			: [];
		const excludeList = !!exclude.value.length
			? exclude.value.split(",").map((s) => s.trim())
			: [];
		const form = new FormData();
		if (!!name.value.length) {
			form.append("name", name.value);
		}
		if (!!include.value.length) {
			form.append("include", JSON.stringify(includeList));
		}
		if (!!exclude.value.length) {
			form.append("exclude", JSON.stringify(excludeList));
		}
		if (duration.value != "0") {
			form.append("duration", duration.value);
		}
		if (rating.value != "0") {
			form.append("rating", rating.value);
		}
		recipes.value = null;
		const request = await fetch("http://localhost:8000/search", {
			body: form,
			method: "POST",
		});
		const response = await request.json();
		recipes.value = response;
	};

	const recipesChosen = computed(() => !!(recipes.value?.length ?? 0));

	const include = ref("");
	const exclude = ref("");
	const rating = ref("0");
	const duration = ref("0");
	// Visualize the duration
	const durationPT = computed(() =>
		// Reference https://stackoverflow.com/questions/1322732/convert-seconds-to-hh-mm-ss-with-javascript
		duration.value === "0"
			? "No maximum"
			: new Date(Number.parseInt(duration.value) * 1000)
					.toISOString()
					.slice(11, 16)
					.replace(":", "h ")
					.concat("m")
	);

	const ratingShow = computed(() =>
		rating.value === "0" ? "No minimum" : rating.value
	);

	const name = ref("");
</script>

<template>
	<div class="grid grid-rows-[auto,1fr] min-h-full w-full">
		<h1 class="text-3xl mb-10 text-center">Recipe Searcher</h1>
		<div class="h-full w-full grid grid-cols-[auto,1fr] gap-10">
			<aside class="h-full border-r-[1px] pe-10 border-white">
				<div class="sticky top-5 left-0">
					<button
						class="mx-auto inline-block mb-5"
						:disabled="!include.length && !name.length"
						@click="searchRecipes">
						Search
					</button>
					<div class="grid gap-5">
						<div>
							<label class="text-sm pb-1 block" for="name">Name</label>
							<input type="text" id="name" v-model="name" />
						</div>
						<div>
							<label class="text-sm pb-1 block" for="to-include">
								Ingredients
							</label>
							<input type="text" id="to-include" v-model="include" />
							<span class="block text-xs pt-1 italic">
								Provide a comma seperated list of ingredients
							</span>
						</div>
						<div>
							<label class="text-sm pb-1 block" for="to-exclude">
								Ingredients to exclude
							</label>
							<input type="text" id="to-exclude" v-model="exclude" />
							<span class="block text-xs pt-1 italic">
								Provide a comma seperated list of ingredients
							</span>
						</div>
						<div>
							<label class="text-sm pb-1 block" for="rating">
								Minimum rating
							</label>
							<div class="flex justify-between">
								<input
									id="rating"
									min="0"
									max="5"
									type="range"
									v-model="rating" />
								<span>{{ ratingShow }}</span>
							</div>
						</div>
						<div>
							<label class="text-sm pb-1 block" for="duration">
								Maximum duration
							</label>
							<div class="flex justify-between">
								<input
									id="duration"
									type="range"
									max="18000"
									step="300"
									v-model="duration" />
								<span>{{ durationPT }}</span>
							</div>
						</div>
					</div>
				</div>
			</aside>
			<main>
				<div v-if="recipesChosen" class="grid gap-5">
					<Recipe
						class="hover:cursor-pointer"
						@click="select(recipe)"
						v-bind="recipe"
						v-for="(recipe, index) in recipes"
						:key="index" />
				</div>
				<span
					v-if="!recipesChosen"
					class="text-2xl text-center my-16 block text-stone-500">
					Search something to get results
				</span>
				<div
					v-show="!!selectedRecipe"
					class="fixed m-auto top-0 left-0 h-full w-full p-20 backdrop-blur-md">
					<div class="relative h-full">
						<div
							class="grid grid-rows-[auto,1fr] shadow-lg bg-stone-800 h-full overflow-y-auto rounded-2xl">
							<img
								class="w-full h-[30vh] object-cover"
								:src="selectedRecipe?.Images ?? imgUrl" />
							<button
								class="absolute top-0 left-0 bg-transparent"
								@click="select(undefined)">
								<img
									class="h-8 w-8 bg-white rounded-2xl"
									src="./assets/close-button-svgrepo-com.svg"
									alt="" />
							</button>
							<div class="grid p-10 grid-rows-[auto,1fr] gap-10">
								<h2 class="text-3xl">{{ selectedRecipe?.Name }}</h2>
								<div class="grid grid-flow-col gap-5">
									<aside>
										<h4 class="text-xl">Ingredients:</h4>
										<ul class="">
											<li
												v-for="ingredient in selectedRecipe?.RecipeIngredientParts"
												:key="ingredient">
												{{ ingredient }}
											</li>
										</ul>
									</aside>
									<section class="">
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
			</main>
		</div>
	</div>
</template>

<style></style>
