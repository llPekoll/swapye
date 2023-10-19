<script lang="ts">
    import { slide } from "svelte/transition";
    import type { Lead } from "$lib/types";
    import { env } from "$lib/env.js";
    import Loading from "$lib/components/Loading.svelte";
    import { page } from "$app/stores";
    const traduction = $page.data.user.traduction;
    export let leads: Lead[] = [];
    export let name = "";
    export let emblem = "";
    export let uuid = "";
    let isOpen = false;
    let state = "idle";
    const toggle = () => (isOpen = !isOpen);

    const export_signle = () => {
        console.log("export_signle");
        state = "loading";
        let filename = `swapye_${name}.xlsx`;
        let xmlHttpRequest = new XMLHttpRequest();
        xmlHttpRequest.onreadystatechange = function () {
            var a;
            if (
                xmlHttpRequest.readyState === 4 &&
                xmlHttpRequest.status === 200
            ) {
                a = document.createElement("a");
                a.href = window.URL.createObjectURL(xmlHttpRequest.response);
                a.download = filename;
                a.style.display = "none";
                document.body.appendChild(a);
                a.click();
            }
        };
        // TODO: -> Change That Quickly
        xmlHttpRequest.open(
            "GET",
            `${env.VITE_BACKEND_DNS}/export/${uuid}/${emblem}`
        );
        xmlHttpRequest.responseType = "blob";
        xmlHttpRequest.send();
        state = "idle";
    };
</script>

<div class="flex text-slate-700">
    <button
        on:click={toggle}
        aria-expanded={isOpen}
        class="text-4xl cursor-pointer"
    >
        <svg
            class="inline"
            style="tran"
            width="20"
            height="20"
            fill="none"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            viewBox="0 0 24 24"
            stroke="currentColor"
        >
            <path d="M9 5l7 7-7 7" />
        </svg>
        {name}
        <p class="inline text-sm text-slate-500">
            {#if leads.length === 0}
                No
            {:else}
                {leads.length}
            {/if}
            {traduction.leads}.
        </p>
    </button>
</div>
{#if isOpen}
    {#each leads as lead, i}
        <ul transition:slide={{ duration: 300 }}>
            <li class="my-2 py-2 bg-slate-300 px-5 rounded-lg mx-10">
                <p class="text-sm italic font-light">
                    {lead.creation_date}
                </p>
                {#if lead.name}
                    <p class="inline text-sm font-light">
                        {traduction.name_lead}:
                    </p>
                    {lead.name},
                {/if}
                {#if lead.email}
                    <p class="inline text-sm font-light">
                        {traduction.email_lead}:
                    </p>
                    {lead.email},
                {/if}
                {#if lead.phone}
                    <p class="inline text-sm font-light">
                        {traduction.phone_lead}:
                    </p>
                    {lead.phone},
                {/if}
                {#if lead.address}
                    <p class="inline text-sm font-light">
                        {traduction.address_personal}:
                    </p>
                    {lead.address},
                {/if}
                {#if Object.keys(lead.extras).length !== 0}
                    <!-- {JSON.stringify(lead.extras?[0][null])} -->
                    {JSON.stringify(lead.extras)}
                {/if}
            </li>
        </ul>
    {/each}
{/if}

{#if leads.length !== 0}
    {#if state == "loading"}
        <button
            class="my-3 bg-slate-400 text-white rounded-lg py-1 px-10 cursor-wait"
            on:click={export_signle}
        >
            <Loading />
        </button>
    {:else}
        <button
            class="my-3 bg-bleu-gris text-white rounded-lg py-1 px-10"
            on:click={export_signle}
        >
            export {name}
        </button>
    {/if}
{/if}

<style>
    svg {
        transition: transform 0.2s ease-in;
    }

    [aria-expanded="true"] svg {
        transform: rotate(0.25turn);
    }
</style>
