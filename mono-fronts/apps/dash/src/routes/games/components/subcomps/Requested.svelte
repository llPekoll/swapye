<script lang="ts">
    import { enhance } from "$app/forms";
    import CheckBox from "$lib/components/CheckBox.svelte";
    import { emblem, requested } from "$lib/stores";
    import { page } from "$app/stores";
    import { toast } from "@zerodevx/svelte-toast";
    import { errorToast, successToast } from "$lib/toastTheme";

    const traduction = $page.data.user.traduction;

    const permission_list: string[] = $page.data.user.rights;

    let requestName = $requested.requestName;
    let requestTel = $requested.requestTel;
    let requestAddress = $requested.requestAddress;
    let isAlwaysWinner = $requested.isAlwaysWinner;
    let canReplay = $requested.canReplay;
    let canReplayToday = $requested.canReplayToday;
    let emailCheck = $requested.emailCheckOverride;

    let submitText = traduction.submit;
    let submitColor = "bleu-gris";
    let cursor = "cursor-pointer";
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
    action="?/requesteds"
    use:enhance={() => {
        submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
        submitColor = "bleu-gris/[.3]";
        cursor = "cursor-not-allowed";
        return async ({ result }) => {
            if (result.type === "success") {
                $requested.requestName = result.data?.requestName;
                $requested.requestTel = result.data?.requestTel;
                $requested.requestAddress = result.data?.requestAddress;
                $requested.isAlwaysWinner = result.data?.isAlwaysWinner;
                $requested.canReplay = result.data?.canReplay;
                $requested.canReplayToday = result.data?.canReplayToday;
                $requested.emailCheckOverride = result.data?.emailCheckOverride;

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

    <CheckBox
        tradsToDisp={traduction.requested_name}
        bind:valueToSet={requestName}
        name="requestName"
        bind:needsUpdate
    />
    <CheckBox
        tradsToDisp={traduction.requested_phone}
        bind:valueToSet={requestTel}
        name="requestTel"
        bind:needsUpdate
    />
    <CheckBox
        tradsToDisp={traduction.requested_address}
        bind:valueToSet={requestAddress}
        name="requestAddress"
        bind:needsUpdate
    />

    <CheckBox
        tradsToDisp={traduction.requested_always_winner}
        bind:valueToSet={isAlwaysWinner}
        name="isAlwaysWinner"
        bind:needsUpdate
    />
    <CheckBox
        tradsToDisp={traduction.requested_can_replay}
        bind:valueToSet={canReplay}
        name="canReplay"
        bind:needsUpdate
    />
    <CheckBox
        tradsToDisp={traduction.requested_can_replay_toda}
        bind:valueToSet={canReplayToday}
        name="canReplayToday"
        bind:needsUpdate
    />
    {#if permission_list.includes("email_validator")}
        <CheckBox
            tradsToDisp={traduction.override_email_check}
            bind:valueToSet={emailCheck}
            name="emailCheck"
            bind:needsUpdate
        />
    {/if}
    <div class="w-full flex items-center justify-center py-5">
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
