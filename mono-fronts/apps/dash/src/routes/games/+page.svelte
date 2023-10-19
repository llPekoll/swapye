<script lang="ts">
    import type { PageData } from "./$types";
    import type { Trads } from "$lib/types";

    import AddAccountCard from "$lib/components/AddAccountCard.svelte";
    import AccountCard from "$lib/components/AccountCard.svelte";
    import { page } from "$app/stores";

    export let data: PageData;

    const traduction = $page.data.trads as Trads;
    const games = data.games.games;
</script>

<svelte:head>
    <title>Games</title>
</svelte:head>
<section class="ml-52">
    <div class="clear-right" />
    <div class="text-center pb-12">
        {#if data.games.length === 0}
            <h2 class="text-base font-bold text-indigo-600">
                {traduction.wellcome}
            </h2>
            <h1 class=" text-xl md:text-2xl font-heading text-gray-900">
                {traduction.add_account}
            </h1>
        {/if}
    </div>
    <div
        class=" px-10 pb-16 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-10"
    >
        {#each games as { emblem, name, type_id, skin_id, type }, i}
            <AccountCard {emblem} {name} {type_id} {skin_id} {i} {type} />
        {/each}
        <button data-test="add-new">
            <a data-sveltekit-preload-data="hover" href="/games/new">
                <AddAccountCard />
            </a>
        </button>
    </div>
</section>
