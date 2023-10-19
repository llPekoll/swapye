<script lang="ts">
    import { enhance } from "$app/forms";
    import DropZone from "$lib/components/DropZone.svelte";
    import CheckBox from "$lib/components/CheckBox.svelte";
    import { emblem, salon } from "$lib/stores/index";
    import { page } from "$app/stores";
    import { toast } from "@zerodevx/svelte-toast";
    import { errorToast, successToast } from "$lib/toastTheme";

    // Vairalbes
    const traduction = $page.data.user.traduction;

    let fullScreenBtn = $salon.fullScreenBtn as boolean;
    let restartBtn = $salon.restartBtn as boolean;
    let automaticRestart = $salon.automaticRestart as boolean;
    let automaticRestartCounterValue =
        $salon.automaticRestartCounterValue as number;
    let soundOveride = $salon.soundOveride as string;

    // DropZone
    let cleared = false;
    const clearUrl = `/perso/clear/${$emblem}/sound`;
    // Form
    let submitColor = "bleu-gris";
    let cursor = "cursor-pointer";
    let submitText = traduction.submit;
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
    action="?/salon"
    use:enhance={({ form }) => {
        submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
        submitColor = "bleu-gris/[.3]";
        cursor = "cursor-not-allowed";
        return async ({ result, update }) => {
            if (result.type === "success") {
                $salon.fullScreenBtn = result.data.fullScreenBtn;
                $salon.restartBtn = result.data.restartBtn;
                $salon.automaticRestart = result.data.automaticRestart;
                $salon.automaticRestartCounterValue =
                    result.data.automaticRestartCounterValue;
                $salon.soundOveride = result.data.soundOveride;

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
    <p>{traduction.waiting_music}</p>

    <DropZone
        fileType="sound"
        name="music"
        src={soundOveride}
        bind:cleared
        {clearUrl}
        bind:needsUpdate
        whatItisToUpload="Music d'attente"
    />

    <CheckBox
        bind:valueToSet={fullScreenBtn}
        bind:needsUpdate
        tradsToDisp="Possibilité de passé en fullscren"
        name="fullscreen_btn"
    />

    <CheckBox
        bind:valueToSet={restartBtn}
        bind:needsUpdate
        tradsToDisp="Possibilité de redemarer le jeux"
        name="restart_btn"
    />

    <CheckBox
        bind:valueToSet={automaticRestart}
        bind:needsUpdate
        tradsToDisp="redemarage automatique du jeux"
        name="automatic_restart"
    />

    {#if automaticRestart}
        <label for="timer" class="text-slate-600 pt-1">
            {traduction.restart_time}

            <input
                class="ml-5 border border-slate-600 rounded-lg px-2 py-1 w-1/3 float-right text-right"
                type="number"
                name="timer"
                on:blur={() => (needsUpdate = true)}
                value={automaticRestartCounterValue}
            />
        </label>
    {/if}
    <div class="flex justify-center items-center mx-auto py-5 w-full" />

    <div class="w-full mx-auto text-center py-5">
        <button
            type="submit"
            class="px-10 py-2 text-white bg-{submitColor} rounded-lg mx-auto text-center w-1/3 flex my-4 shadow-lg shadow-{submitColor} font-bold {cursor}"
            {disabled}
        >
            <p class="text-center mx-auto">
                {@html submitText}
            </p>
        </button>
    </div>
</form>
