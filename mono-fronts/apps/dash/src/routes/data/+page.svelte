<script lang="ts">
    import { env } from "$lib/env.js";
    import type { PageData } from "./$types";
    import GameTab from "./components/GameTab.svelte";
    import { page } from "$app/stores";

    export let data: PageData;

    const traduction = $page.data.user.traduction;
    const leads = data.leads;
    const uuid = data.uuid;

    const exportData = () => {
        let filename = "TestReport.xlsx";
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
        xmlHttpRequest.open("GET", `${env.VITE_BACKEND_DNS}/export/${uuid}`);
        xmlHttpRequest.responseType = "blob";
        xmlHttpRequest.send();
    };
</script>

<svelte:head>
    <title>Leads.</title>
</svelte:head>
<section class="ml-52 grid grid-cols-2 gap-4">
    <div class="leads overflow-scroll pt-10">
        <div class=" italic text-slate-400  font-bold text-7xl">
            {leads.total_leads}
            <span class=" font-bold text-3xl italic -ml-5 text-slate-700">
                {traduction.leads}:
            </span>
        </div>
        <ul class="ml-5">
            {#each leads.signe_leads as lead}
                <GameTab
                    leads={lead.leads}
                    name={lead.name}
                    emblem={lead.emblem}
                    {uuid}
                />
            {/each}
        </ul>
    </div>
    <button>
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <p
            on:click={exportData}
            class="bg-slate-200 py-2 w-1/3 mx-auto rounded-lg shadow"
        >
            {traduction.export} All
        </p>
    </button>
</section>

<style>
    .leads {
        height: 100vh;
    }
</style>
