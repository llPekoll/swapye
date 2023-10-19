<script lang="ts">
    import type { Price } from "$lib/types";
    import { page } from "$app/stores";
    import Chart from "./Chart.svelte";
    import { prices as priceStore } from "$lib/stores";

    const traduction = $page.data.user.traduction;
    let prices = $priceStore.prices as Price[];
    let playerNumber = 0;
    for (let i = 0; i < prices.length; i++) {
        console.log(prices[i]);
        console.log(prices[i].price_left);
        playerNumber += prices[i].price_won!;
    }
</script>

<svelte:head>
    <title>{traduction.title_game_info}</title>
</svelte:head>
<section class="pl-10">
    <img src="/prices.svg" class="text-center w-44 inline mt-10" alt="basics" />
    <p class="align-bottom inline text-5xl font-bold italic text-slate-400">
        {traduction.title_game_info}
    </p>
    <div class="py-10">
        <p class="text-center font-light text-xl py-5 text-slate-700">
            {traduction.info_number_total}
            <span class="block text-7xl italic text-slate-900 font-bold -mt-3"
                >{playerNumber}</span
            >
        </p>
    </div>
    <div class="py-10">
        <div class="flex flex-wrap">
            {#each prices as price}
                <div
                    class="bg-slate-300 rounded-lg p-8 w-1/5 m-2 shadow-lg min-fit"
                >
                    <p class="block">{price.name}:</p>
                    <p class="pl-5">{price.price_won}/{price.number}</p>
                    <div class="scale-100">
                        <Chart left={price.price_won} total={price.number} />
                    </div>
                </div>
            {/each}
        </div>
    </div>
</section>

<style>
    .min-fit {
        min-width: 18rem;
    }
</style>
