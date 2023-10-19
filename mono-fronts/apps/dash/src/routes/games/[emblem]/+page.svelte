<script lang="ts">
    import type { PageData } from "./$types";
    import type { Price as PriceTypes } from "$lib/types";

    import {
        emblem,
        dryRun,
        basics,
        prices,
        dateNregion,
        salon,
        identity,
        forms,
        requested,
        extraReqReturn,
    } from "$lib/stores";
    import { page } from "$app/stores";
    import { fly } from "svelte/transition";
    import Info from "./../components/Info.svelte";
    import Analytics from "./../components/Analytics.svelte";
    import GameEdit from "../components/GameEdit.svelte";
    import Prices from "./../components/Prices.svelte";
    import Perso from "./../components/Perso.svelte";

    import Test from "./../components/Test.svelte";

    export let data: PageData;

    const traduction = $page.data.user.traduction;
    const link: string = data.game.link;
    const qr_location: string = data.game.qr_location;
    console.log("data", data.prices.prices);
    emblem.set(data.game.emblem);
    basics.set(data.basics);
    dryRun.set(data.dryRun);
    prices.set(data.prices);
    dateNregion.set(data.date);
    salon.set(data.salon);
    identity.set(data.identity);
    forms.set(data.form);
    requested.set(data.requesteds);
    extraReqReturn.set(data.extrarequesteds);

    let timeZones: string[] = data.game.time_zones;

    let menuState = 0;
    function handleAnchorClick(scrollerTarget: string) {
        const anchor = document.getElementById(scrollerTarget);

        window.scrollTo({
            top: anchor?.offsetTop,
            behavior: "smooth",
        });
    }
</script>

<section class="ml-12">
    <ul
        class="pt-24 float-left fixed bg-bleu-gris/50 pl-12 {menuState === 0
            ? 'pr-6'
            : 'pr-8'} h-screen text-white font-bold text-2xl italic rounded-tr-3xl"
    >
        <li
            class="cursor-pointer {menuState === 1 ? 'selected' : ''}"
            on:click={() => (menuState = 1)}
            on:keypress={() => (menuState = 1)}
            data-test="menu-basics"
        >
            {traduction.menu_game_basics}
        </li>
        <li
            class="cursor-pointer {menuState === 0 ? 'selected' : ''}"
            on:click={() => (menuState = 0)}
            on:keypress={() => (menuState = 0)}
            data-test="menu-perso"
        >
            {traduction.menu_game_perso}
            {#if menuState === 0}
                <ol class="list-decimal ml-10 font-normal text-base text-white">
                    <li
                        class="cursor-pointer"
                        on:click={() => handleAnchorClick("#anchor-date")}
                        on:keypress={() => handleAnchorClick("#anchor-date")}
                        data-test="menu-date"
                    >
                        {traduction.date_preso_title}
                    </li>

                    <li
                        class="cursor-pointer"
                        on:click={() => handleAnchorClick("#anchor-salon")}
                        on:keypress={() => handleAnchorClick("#anchor-salon")}
                        data-test="menu-salon"
                    >
                        {traduction.titlte_perso_event}
                    </li>

                    <li
                        class="cursor-pointer"
                        on:click={() => handleAnchorClick("#anchor-id")}
                        on:keypress={() => handleAnchorClick("#anchor-id")}
                        data-test="menu-id"
                    >
                        {traduction.company_preso_title}
                    </li>
                    <li
                        class="cursor-pointer"
                        on:click={() => handleAnchorClick("#anchor-form")}
                        on:keypress={() => handleAnchorClick("#anchor-form")}
                        data-test="menu-form"
                    >
                        {traduction.titlte_perso_forms}
                    </li>

                    <li
                        class="cursor-pointer"
                        on:click={() => handleAnchorClick("#anchor-requested")}
                        on:keypress={() =>
                            handleAnchorClick("#anchor-requested")}
                        data-test="menu-requested"
                    >
                        {traduction.required_preso_title}
                    </li>
                    <li
                        class="cursor-pointer"
                        on:click={() => handleAnchorClick("#anchor-extras")}
                        on:keypress={() => handleAnchorClick("#anchor-extras")}
                        data-test="menu-extras"
                    >
                        {traduction.extra_preso_title}
                    </li>
                </ol>
            {/if}
        </li>
        <li
            class="cursor-pointer {menuState === 4 ? 'selected' : ''}"
            on:click={() => (menuState = 4)}
            on:keypress={() => (menuState = 4)}
            data-test="menu-prices"
        >
            {traduction.menu_game_prices}
        </li>
        <li
            class="cursor-pointer {menuState === 2 ? 'selected' : ''}"
            on:click={() => (menuState = 2)}
            on:keypress={() => (menuState = 2)}
            data-test="menu-analitycs"
        >
            {traduction.menu_game_analitycs}
        </li>
        <li
            class="cursor-pointer {menuState === 3 ? 'selected' : ''}"
            on:click={() => (menuState = 3)}
            on:keypress={() => (menuState = 3)}
            data-test="menu-info"
        >
            {traduction.menu_game_info}
        </li>
        <li
            class="cursor-pointer {menuState === 5 ? 'selected' : ''}"
            on:click={() => (menuState = 5)}
            on:keypress={() => (menuState = 5)}
            data-test="menu-test"
        >
            {traduction.menu_test}
        </li>
    </ul>
    <div class="inline">
        {#if menuState === 0}
            <div in:fly={{ y: 100 }} class="px-20 pb-6 ml-52">
                <Perso {timeZones} />
            </div>
        {:else if menuState === 1}
            <div in:fly={{ y: 100 }} class="px-20 pb-6 ml-44">
                <GameEdit />
            </div>
        {:else if menuState === 2}
            <div in:fly={{ y: 100 }} class="px-20 pb-6 ml-44">
                <Analytics />
            </div>
        {:else if menuState === 3}
            <div in:fly={{ y: 100 }} class="px-20 pb-6 ml-44">
                <Info {qr_location} {link} />
            </div>
        {:else if menuState === 4}
            <div in:fly={{ y: 100 }} class="px-20 pb-6 ml-44">
                <Prices />
            </div>
        {:else if menuState === 5}
            <div in:fly={{ y: 100 }} class="px-20 pb-6 ml-44">
                <Test />
            </div>
        {/if}
    </div>
</section>

<style>
    .selected {
        color: #ffc351;
    }
</style>
