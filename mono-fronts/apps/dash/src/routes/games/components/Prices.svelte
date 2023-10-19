<script lang="ts">
    import AddAccountCard from "$lib/components/AddAccountCard.svelte";
    import NewPrice from "./NewPrice.svelte";
    import type { Price, TimeTable } from "$lib/types";
    import CheckBox from "$lib/components/CheckBox.svelte";
    import { emblem, prices as priceStore, dateNregion } from "$lib/stores";
    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import { fly } from "svelte/transition";

    const traduction = $page.data.user.traduction;
    let prices = $priceStore.prices as Price[];
    let priceName = "";
    let langs = $priceStore.langs as unknown as { lang: string }[];
    let enableQr = $priceStore.enableQr as boolean;
    let updateTitles = false;

    const addPrice = () => {
        let newPrice: Price = {
            name: "New Price",
            number: 0,
            img: "",
            id: 0,
            displayPriceName: true,
            emailTemplate: 0,
            timetable: [] as TimeTable[],
            consolationPrice: false,
            extra_langs: langs,
            tradPacks: [
                {
                    lang: langs[0].lang,
                    src: "",
                    name: "new price",
                },
            ],
        };

        prices = [...prices, newPrice];
        selectedPrice = prices.length - 1;
    };
    let days: string[] = [];
    let isLoading = false; // wait for the timetable to be fetched
    onMount(async () => {
        if (!$dateNregion.unlimitedInTime) {
            isLoading = true;
            const res = await fetch(`/perso/${$emblem}/timeframe`);
            const re = await res.json();
            days = re.days;
            isLoading = false;
        }
    });

    const temp = `*pour utiliser cette feature il vous faudra ajouter {{var:qr_location:""}}`;
    const updateQr = async (enableQr: boolean) => {
        const res = await fetch(`/prices/qr/${$emblem}`, {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ enable_qr: enableQr }),
        });
        const re = await res.json();
        priceStore.update((p) => {
            p.enableQr = re.enable_qr;
            return p;
        });
    };
    $: updateQr(enableQr);
    let selectedPrice = 0;
    $: if (updateTitles) {
        prices[selectedPrice].name = priceName;
        updateTitles = false;
    }
</script>

<svelte:head>
    <title>{traduction.game_price_title}</title>
</svelte:head>
<section class="mx-10">
    <div class=" pt-10">
        <img src="/prices.svg" class="text-center w-44 inline" alt="basics" />
        <p class="align-bottom inline text-5xl font-bold italic text-slate-400">
            {traduction.game_price_title}
        </p>
    </div>
    <div class="flex">
        <button on:click={addPrice} class="pt-10 w-80 text-center">
            <AddAccountCard />
        </button>
        <div class=" py-10 inline w-full justify-end text-right pr-6">
            <CheckBox
                tradsToDisp="Utiliser la recuperation de Qr code pour le jeux"
                bind:valueToSet={enableQr}
                name="enableQr"
            />
            {@html temp}
        </div>
    </div>

    <div class="flex">
        <ol class="">
            {#each prices as price, i}
                <li
                    on:click={() => (selectedPrice = i)}
                    on:keypress={() => (selectedPrice = i)}
                    class="{i == selectedPrice
                        ? 'bg-bleu-gris text-white italic font-bold'
                        : 'bg-slate-200'} 
                        rounded-lg shadow-lg my-2 py-2 w-60 pl-3 cursor-pointer"
                >
                    <button>
                        {i + 1}.{price.name}
                    </button>
                </li>
            {/each}
        </ol>
        {#each prices as price, i}
            {#if i == selectedPrice}
                <div
                    in:fly={{ y: -50 }}
                    class="w-full px-4"
                    on:focus={() => (updateTitles = true)}
                >
                    <NewPrice
                        bind:priceName
                        {price}
                        {days}
                        {langs}
                        updaloed={true}
                        bind:isLoading
                        bind:updateTitles
                    />
                </div>
            {/if}
        {/each}
    </div>
</section>
<div class="pl-4">
    ***{traduction.jackpot_warning}
    <br />
    * {traduction.price_fill_api_key}
    <br />
    ** {traduction.price_consolation_price_explaine}
</div>

<style>
    section {
        min-height: 200px;
    }
</style>
