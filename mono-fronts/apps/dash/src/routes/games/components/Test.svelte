<script lang="ts">
    import { enhance } from "$app/forms";
    import { emblem } from "$lib/stores/index";
    import { page } from "$app/stores";
    import CheckBox from "$lib/components/CheckBox.svelte";
    import { dryRun as dryRunStore } from "$lib/stores";
    import { toast } from "@zerodevx/svelte-toast";
    import { errorToast, successToast } from "$lib/toastTheme";
    // import { submitUpdater } from "$lib/utils";

    const traduction = $page.data.user.traduction;
    let forceResultWon = $dryRunStore.forceResultWon;
    let forceResultLost = $dryRunStore.forceResultLost;
    let forceResultCantReplay = $dryRunStore.forceResultCantReplay;
    let forceResultCantReplayToday = $dryRunStore.forceResultCantReplayToday;
    let dryRun = $dryRunStore.dryRun;
    let submitText = traduction.submit;
    let submitColor = "bleu-gris";
    let cursor = "cursor-pointer";
    let needsUpdate = false;
    let disabled = true;
    $: disabledbtn = !dryRun;
    $: if (!dryRun) {
        forceResultWon = false;
        forceResultLost = false;
        forceResultCantReplay = false;
        forceResultCantReplayToday = false;
    }
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

<svelte:head>
    <title>{traduction.menu_test}</title>
</svelte:head>
<section class=" p-10">
    <img src="/test.svg" class="text-center w-44 inline" alt="basics" />
    <p class="align-bottom inline text-5xl font-bold italic text-slate-400">
        {traduction.menu_test}
    </p>
    <form
        class="w-full px-10 pt-10"
        method="POST"
        action="?/dryrun"
        use:enhance={({ form }) => {
            submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
            submitColor = "bleu-gris/[.3]";
            cursor = "cursor-not-allowed";
            return async ({ result }) => {
                if (result.type === "success") {
                    $dryRunStore.forceResultWon = result.data?.forceResultWon;
                    $dryRunStore.forceResultLost = result.data?.forceResultLost;
                    $dryRunStore.forceResultCantReplay =
                        result.data?.forceResultCantReplay;
                    $dryRunStore.forceResultCantReplayToday =
                        result.data?.forceResultCantReplayToday;
                    $dryRunStore.dryRun = result.data?.dryRun;

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
        <!-- dryRun -->

        <CheckBox
            tradsToDisp={traduction.dryrun_is_test}
            bind:valueToSet={dryRun}
            bind:needsUpdate
            name="dryRun"
        />
        <p class="text-sm -mt-2 ml-2 text-slate-400 mb-10">
            *{traduction.dryrun_dryrun}
        </p>
        <div class={dryRun ? "" : "opacity-30"}>
            <button
                type="button"
                class="w-full text-left"
                on:click={() => {
                    forceResultLost = false;
                    forceResultCantReplay = false;
                    forceResultCantReplayToday = false;
                }}
            >
                <CheckBox
                    tradsToDisp={traduction.dryrun_forceResultWon}
                    bind:valueToSet={forceResultWon}
                    bind:needsUpdate
                    name="forceResultWon"
                    bind:disabled={disabledbtn}
                />
            </button>
            <button
                type="button"
                class="w-full text-left"
                on:click={() => {
                    forceResultWon = false;
                    forceResultCantReplay = false;
                    forceResultCantReplayToday = false;
                }}
            >
                <CheckBox
                    tradsToDisp={traduction.dryrun_forceResultLost}
                    bind:valueToSet={forceResultLost}
                    bind:needsUpdate
                    name="forceResultLost"
                    bind:disabled={disabledbtn}
                />
            </button>

            <button
                type="button"
                class="w-full text-left"
                on:click={() => {
                    forceResultWon = false;
                    forceResultLost = false;
                    forceResultCantReplayToday = false;
                }}
            >
                <CheckBox
                    tradsToDisp={traduction.dryrun_forceResultCantReplay}
                    bind:valueToSet={forceResultCantReplay}
                    name="forceResultCantReplay"
                    bind:needsUpdate
                    bind:disabled={disabledbtn}
                />
            </button>
            <button
                type="button"
                class="w-full text-left"
                on:click={() => {
                    forceResultWon = false;
                    forceResultLost = false;
                    forceResultCantReplay = false;
                }}
            >
                <CheckBox
                    tradsToDisp={traduction.dryrun_forceResultCantReplayToda}
                    bind:valueToSet={forceResultCantReplayToday}
                    name="forceResultCantReplayToday"
                    bind:needsUpdate
                    bind:disabled={disabledbtn}
                />
            </button>
        </div>
        <div class="w-full flex items-center justify-center py-5">
            <button
                type="submit"
                class="px-10 py-2 text-white bg-{submitColor} rounded-lg mx-auto text-center w-1/3 flex my-4 shadow-lg shadow-{submitColor} font-bold {cursor} "
                {disabled}
                data-test="submit"
            >
                <p class="text-center mx-auto">
                    {@html submitText}
                </p>
            </button>
        </div>
    </form>
</section>
