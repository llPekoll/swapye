<script lang="ts">
    import type { PageData } from "./$types";
    import type { Trads } from "$lib/types";
    import Loading from "$lib/components/Loading.svelte";
    import { page } from "$app/stores";
    export let data: PageData;

    interface Result {
        message: string;
        status: string;
    }
    const traduction = $page.data.user.traduction as Trads;
    const result: Result = data.result;
    const message: string = result.message;
    const status: string = result.status;
    let okMessage: string = "";
    let loading = false;
    const validate = async () => {
        loading = true;
        const res = await fetch(
            `${$page.url.origin}/unlock/price/${$page.params.unlockcode}`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );
        const result = await res.json();
        if (result.success == true) {
            okMessage = "Validated";
        }
        loading = false;
    };
</script>

<svelte:head>
    <title>Unlock Price</title>
</svelte:head>

<section class="flex h-screen items-center justify-center text-center">
    <div class="py-10">
        {#if status == "success" && okMessage == ""}
            <div
                class="{status == 'success'
                    ? 'text-red-500'
                    : 'text-green-500'} text-3xl align-center"
            >
                {@html message}
            </div>
            <button
                on:click={validate}
                class="bg-slate-200 py-2 mx-auto rounded-lg shadow px-10 w-100 mt-10"
            >
                {#if loading}
                    <Loading />
                {:else}
                    {traduction.validate_price}
                {/if}
            </button>
        {/if}
        {#if okMessage}
            <p>{okMessage}</p>
            <button
                class="bg-slate-200 py-2 mx-auto rounded-lg shadow px-10 w-100 mt-10"
                on:click={() => {
                    location.reload();
                }}
            >
                reload
            </button>
        {/if}
    </div>
</section>
