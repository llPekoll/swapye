<script lang="ts">
    import { enhance } from "$app/forms";
    import Input from "$lib/components/Input.svelte";
    import { page } from "$app/stores";
    import { toast } from "@zerodevx/svelte-toast";
    import { errorToast, successToast } from "$lib/toastTheme";
    import { personals } from "$lib/stores";

    // Variables
    const traduction = $page.data.user.traduction;
    let name = $personals.name;
    let address = $personals.address;
    let postal = $personals.postal;
    let city = $personals.city;
    let emailContact = $personals.conact_email;
    let companyName = $personals.company_name;
    let rib = $personals.rib;
    let siret = $personals.siret;
    let phone = $personals.phone;

    // Form
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

<div class="my-2 px-5 mx-10">
    <form
        class="py-6"
        method="POST"
        action="?/personal"
        use:enhance={() => {
            submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
            submitColor = "bleu-gris/[.3]";
            cursor = "cursor-not-allowed";
            return async ({ result }) => {
                if (result.type === "success") {
                    $personals.name = result.data?.name;
                    $personals.address = result.data?.address;
                    $personals.postal = result.data?.postal;
                    $personals.city = result.data?.city;
                    $personals.conact_email = result.data?.conact_email;
                    $personals.company_name = result.data?.company_name;
                    $personals.rib = result.data?.rib;
                    $personals.siret = result.data?.siret;
                    $personals.phone = result.data?.phone;
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
        <Input
            name={traduction.fullName}
            bind:val={name}
            inputName="name"
            bind:needsUpdate
        />
        <Input
            name={traduction.address_personal}
            bind:val={address}
            inputName="address"
            bind:needsUpdate
        />
        <Input
            name={traduction.postal_personal}
            bind:val={postal}
            inputName="postal"
            bind:needsUpdate
        />
        <Input
            name={traduction.town_personal}
            bind:val={city}
            inputName="city"
            bind:needsUpdate
        />
        <Input
            name="Email de contact"
            bind:val={emailContact}
            inputName="emailContact"
            bind:needsUpdate
        />
        <Input
            name="Nom de la companie"
            bind:val={companyName}
            inputName="companyName"
            bind:needsUpdate
        />
        <Input name="Rib" bind:val={rib} inputName="rib" bind:needsUpdate />
        <Input
            name="No Siret"
            bind:val={siret}
            inputName="siret"
            bind:needsUpdate
        />
        <Input
            name="Téléphone"
            bind:val={phone}
            inputName="phone"
            bind:needsUpdate
        />

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
<div class="bg-slate-500" />
