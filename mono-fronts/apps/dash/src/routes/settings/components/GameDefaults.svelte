<script lang="ts">
    import { page } from "$app/stores";
    import { enhance } from "$app/forms";
    import CheckBox from "$lib/components/CheckBox.svelte";
    import DropZone from "$lib/components/DropZone.svelte";
    import { toast } from "@zerodevx/svelte-toast";
    import { errorToast, successToast } from "$lib/toastTheme";
    import { defaults } from "$lib/stores";

    // variables

    const rights: string[] = $page.data.user.rights;
    const traduction = $page.data.user.traduction;

    let emailCheck = $defaults.email_check;
    let srcLogo = $defaults.logo;
    let srcSound = $defaults.music;

    // Forms
    let cursor = "cursor-pointer";
    let submitText = traduction.submit;
    let submitColor = "bleu-gris";

    // DropZone
    const clearLogo = `/perso/clear/defautls/logo`;
    let clearedLogo = false;
    const clearSound = `/perso/clear/defautls/sound`;
    let clearedSound = false;
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

<div class="py-2 px-5 mx-10">
    <form
        class="py-6"
        method="POST"
        action="?/gameDefaults"
        use:enhance={({ form }) => {
            submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
            submitColor = "bleu-gris/[.3]";
            cursor = "cursor-not-allowed";
            return async ({ result }) => {
                if (result.type === "success") {
                    $defaults.email_check = result.data?.email_check;
                    $defaults.logo = result.data?.logo;
                    $defaults.music = result.data?.music;

                    toast.push(traduction.toast_success, { ...successToast });
                }
                if (result.type === "error") {
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
        <div id="#anchor-form">
            <p class="text-center text-3xl font-bold text-slate-800">
                {traduction.logo_default}
            </p>
            <DropZone
                fileType="image"
                name="logo"
                src={srcLogo}
                clearUrl={clearLogo}
                bind:cleared={clearedLogo}
                whatItisToUpload="Logo"
                bind:needsUpdate
            />
            <div class="pt-10 pb-16">
                <p class="text-center text-3xl font-bold text-slate-800">
                    {traduction.music_default}
                </p>
                <DropZone
                    fileType="sound"
                    name="music"
                    src={srcSound}
                    clearUrl={clearSound}
                    bind:cleared={clearedSound}
                    whatItisToUpload="Music d'attente"
                    bind:needsUpdate
                />
            </div>
        </div>
        {#if rights.includes("email_validator")}
            <div id="#anchor-emails">
                <CheckBox
                    bind:valueToSet={emailCheck}
                    tradsToDisp={traduction.default_email_check}
                    name="email_check"
                    bind:needsUpdate
                />
            </div>
        {/if}

        <button
            type="submit"
            class="px-10 py-2 text-white bg-{submitColor} rounded-lg mx-auto text-center w-1/3 flex my-4 shadow-lg shadow-{submitColor} font-bold {cursor}"
            data-test="submit"
            {disabled}
        >
            <p class="text-center mx-auto">
                {@html submitText}
            </p>
        </button>
    </form>
</div>
