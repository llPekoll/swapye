<script lang="ts">
    import MultiSelect from "svelte-multiselect";

    import { enhance } from "$app/forms";
    import { requested } from "$lib/stores/requested";
    import CheckBox from "$lib/components/CheckBox.svelte";
    import { fly } from "svelte/transition";
    import { emblem, dateNregion } from "$lib/stores";
    import { page } from "$app/stores";
    import { toast } from "@zerodevx/svelte-toast";
    import { errorToast, successToast } from "$lib/toastTheme";
    export let timeZones: string[];

    const traduction = $page.data.user.traduction;
    let startDate = $dateNregion.startDate
        ? new Date($dateNregion.startDate).toISOString().split(".")[0]
        : "";
    let endDate = $dateNregion.endDate
        ? new Date($dateNregion.endDate).toISOString().split(".")[0]
        : "";
    console.log($dateNregion.startHour);
    let startHour = $dateNregion.startHour;
    let endHour = $dateNregion.endHour;
    let unlimitedInTime = $dateNregion.unlimitedInTime;
    let losingFactor = $dateNregion.losingFactor;
    let timeZone = $dateNregion.timeZone;
    let selected: string[] = $dateNregion.extraLangs.map(
        (x: { lang: string }) => x.lang
    );

    const ui_libs = [
        `🇫🇷 France`,
        `🇬🇧 Anglais`,
        `🇪🇸 Espagnol`,
        `🇮🇹 Italien`,
        `🇩🇪 Allemand`,
        `🇨🇳 Chinois`,
    ];
    $: sesel = JSON.stringify(selected);
    let cursor = "cursor-pointer";
    let submitText = traduction.submit;
    let submitColor = "bleu-gris";
    let needsUpdate = false;
    let disabled = true;
    $: if (needsUpdate) {
        submitText = traduction.submit;
        submitColor = "bleu-gris";
        cursor = "cursor-pointer";
        disabled = false;
    } else {
        submitText = traduction.submit;
        submitColor = "bleu-gris/[.3]";
        cursor = "cursor-not-allowed";
        disabled = true;
    }
</script>

<form
    class="w-full px-10 pt-10"
    enctype="multipart/form-data"
    method="POST"
    action="?/date"
    use:enhance={({ form }) => {
        submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
        submitColor = "bleu-gris/[.3]";
        cursor = "cursor-not-allowed";
        return async ({ result }) => {
            if (result.type === "success") {
                $dateNregion.startDate = result.data?.startDate;
                $dateNregion.endDate = result.data?.endDate;
                $dateNregion.startHour = result.data?.startHour;
                $dateNregion.endHour = result.data?.endHour;
                $dateNregion.unlimitedInTime = result.data?.unlimitedInTime;
                $dateNregion.losingFactor = result.data?.losingFactor;
                $dateNregion.timeZone = result.data?.timeZone;
                $dateNregion.extraLangs = result.data?.extraLangs;

                toast.push(traduction.toast_success, { ...successToast });
            } else {
                toast.push(
                    `${traduction.toast_error}, ${result.error.message}`,
                    {
                        ...errorToast,
                    }
                );
            }
            needsUpdate = false;
        };
    }}
>
    <input type="hidden" name="emblem" value={$emblem} />
    <input type="hidden" name="extra-langs" value={sesel} />
    <label for="margin" class="text-slate-600">{traduction.date_timezone}</label
    >
    <div
        on:click={() => (needsUpdate = true)}
        on:keypress={() => (needsUpdate = true)}
    >
        <select
            name="timeZone"
            value={timeZone}
            class="float-right py-1.5 rounded-md border border-gray-300 pl-3"
        >
            {#each timeZones as timZon}
                <option value={timZon} class="text-slate-600">{timZon}</option>
            {/each}
        </select>
    </div>
    <br />
    <h2 class="my-4">
        Languages = {JSON.stringify(selected).slice(1, -1)}
    </h2>
    <div
        on:click={() => (needsUpdate = true)}
        on:keypress={() => (needsUpdate = true)}
    >
        <MultiSelect bind:selected options={ui_libs} />
    </div>
    <CheckBox
        tradsToDisp="Jeu illimité ds le temps"
        bind:valueToSet={unlimitedInTime}
        name="unlimitedInTime"
        bind:needsUpdate
    />
    {#if !unlimitedInTime}
        <div in:fly={{ x: 100 }} class="grid grid-cols-2 gap-4">
            <div class="">
                <div class="py-3">
                    <label for="startDate" class="text-slate-600">
                        {traduction.date_start}<br />
                        <div
                            on:click={() => (needsUpdate = true)}
                            on:keypress={() => (needsUpdate = true)}
                        >
                            <input
                                type="datetime-local"
                                name="startDate"
                                class="bg-gray-200 appearance-none border-2 border-gray-200 rounded py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
                                value={startDate}
                            />
                        </div>
                    </label>
                </div>
                <div>
                    <label for="endDate" class="text-slate-600">
                        {traduction.date_end} <br />
                        <div
                            on:click={() => (needsUpdate = true)}
                            on:keypress={() => (needsUpdate = true)}
                        >
                            <input
                                type="datetime-local"
                                name="endDate"
                                class="bg-gray-200 appearance-none border-2 border-gray-200 rounded py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
                                value={endDate}
                            />
                        </div>
                    </label>
                </div>
            </div>
            <div class="">
                <div class="py-3">
                    <label for="startDate" class="text-slate-600">
                        {traduction.date_start_day}<br />
                        <div
                            on:click={() => (needsUpdate = true)}
                            on:keypress={() => (needsUpdate = true)}
                        >
                            <input
                                type="time"
                                name="startHour"
                                class="bg-gray-200 appearance-none border-2 border-gray-200 rounded py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
                                value={startHour}
                            />
                        </div>
                    </label>
                </div>
                <div>
                    <label for="endDate" class="text-slate-600">
                        {traduction.date_end_day} <br />
                        <div
                            on:click={() => (needsUpdate = true)}
                            on:keypress={() => (needsUpdate = true)}
                        >
                            <input
                                type="time"
                                name="endHour"
                                class="bg-gray-200 appearance-none border-2 border-gray-200 rounded py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
                                value={endHour}
                            />
                        </div>
                    </label>
                </div>
            </div>
        </div>
    {:else}
        <div in:fly={{ x: 100 }} class="py-3">
            {#if $requested.isAlwaysWinner}
                <p class="italic font-bold ml-20 text-slate-800">
                    {traduction.requested_always_winner}
                </p>

                <input type="hidden" name="losingFactor" value="100" />
            {:else}
                <label for="losingFactor" class="text-slate-600">
                    {traduction.date_lostfactor} <br />
                    <div
                        on:click={() => (needsUpdate = true)}
                        on:keypress={() => (needsUpdate = true)}
                    >
                        <input
                            type="number"
                            name="losingFactor"
                            class="bg-gray-200 appearance-none border-2 border-gray-200 rounded py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
                            bind:value={losingFactor}
                            on:blur={() => {
                                if (losingFactor < 0) losingFactor = 0;
                                if (losingFactor > 100) losingFactor = 100;
                            }}
                        />
                    </div>
                </label>
            {/if}
        </div>
    {/if}
    <div class="w-full flex items-center justify-center py-5">
        <button
            type="submit"
            class="px-10 py-2 text-white bg-{submitColor} rounded-lg mx-auto text-center w-1/3 flex my-4 shadow-lg shadow-{submitColor} font-bold {cursor}"
            {disabled}
            data-test="submit"
        >
            <p class="text-center mx-auto">
                {@html submitText}
            </p>
        </button>
    </div>
</form>

<style>
    :global(div.multiselect) {
        background-color: white;
    }
</style>
