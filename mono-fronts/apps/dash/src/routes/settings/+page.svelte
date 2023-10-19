<script lang="ts">
    import type { PageData } from "./$types";
    import { fly } from "svelte/transition";
    import { page } from "$app/stores";
    import FormPersonal from "./components/FormPersonal.svelte";
    import FormApiKey from "./components/FormApiKey.svelte";
    import GameDefaults from "./components/GameDefaults.svelte";
    import { apiKey, defaults, personals } from "$lib/stores";
    // import RGPDs from "./components/RGPDs.svelte";

    const traduction = $page.data.user.traduction;
    export let data: PageData;
    apiKey.set(data.apiKey);
    defaults.set(data.defaults);
    personals.set(data.personals);

    let menuState = 0;
</script>

<svelte:head>
    <title>{traduction.menu_settings}</title>
</svelte:head>

<section class="ml-36 -mt-2">
    <ul
        class="pt-24 float-left fixed bg-bleu-gris/50 pl-12 h-screen text-white font-bold text-2xl italic pr-8"
    >
        <li
            class="cursor-pointer {menuState === 0 ? 'selected' : ''}"
            on:click={() => (menuState = 0)}
            on:keypress={() => (menuState = 0)}
            data-test="menu-personals"
        >
            {traduction.personals}
        </li>
        <li
            class="cursor-pointer {menuState === 1 ? 'selected' : ''}"
            on:click={() => (menuState = 1)}
            on:keypress={() => (menuState = 1)}
            data-test="menu-api"
        >
            {traduction.email_apikey}
        </li>
        <li
            class="cursor-pointer {menuState === 2 ? 'selected' : ''}"
            on:click={() => (menuState = 2)}
            on:keypress={() => (menuState = 2)}
            data-test="defaults"
        >
            {traduction.game_defaults}
        </li>
    </ul>
    <div class="inline">
        {#if menuState === 0}
            <div in:fly={{ y: -100 }} class="px-4 pb-6 ml-48">
                <FormPersonal />
            </div>
        {:else if menuState === 1}
            <div in:fly={{ y: -100 }} class="px-4 pb-6 ml-48">
                <FormApiKey />
            </div>
        {:else if menuState === 2}
            <div in:fly={{ y: -100 }} class="px-4 pb-6 ml-48">
                <GameDefaults />
            </div>
            <!-- {:else if menuState === 3}
            <div in:fly={{ y: -100 }} class="px-4 pb-6 ml-48">
                <RGPDs {trads} {regulation} {policyRules} />
            </div> -->
        {/if}
    </div>
</section>

<style>
    .selected {
        color: #ffc351;
    }
</style>
