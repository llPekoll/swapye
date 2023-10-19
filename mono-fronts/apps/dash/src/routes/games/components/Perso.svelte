<script lang="ts">
    import ID from "./subcomps/ID.svelte";
    import Date from "./subcomps/Date.svelte";
    import Requested from "./subcomps/Requested.svelte";
    import ExtraRequesteds from "./subcomps/ExtraRequesteds.svelte";
    import SalonMode from "./subcomps/SalonMode.svelte";
    import Form from "./subcomps/Form.svelte";
    import { page } from "$app/stores";

    export let timeZones: string[];
    const traduction = $page.data.user.traduction;
    let windowScrollY = 0;
</script>

<svelte:head>
    <title>{traduction.game_edit_title}</title>
</svelte:head>
<svelte:window bind:scrollY={windowScrollY} />
<section class="w-full">
    <div id="#anchor-date">
        <img
            src="/date.svg"
            class="text-center w-44 pt-10 inline ml-10"
            alt="date"
        />
        <p
            class="align-bottom inline text-5xl font-bold italic text-slate-400 -ml-10"
        >
            {traduction.date_preso_title}
        </p>
        <Date {timeZones} />
    </div>
    <div
        class="w-3/4 border-b-4 border-salte-200 text-center mx-auto mb-20 mt-10"
    />
    <div id="#anchor-salon">
        <img
            src="/salon.svg"
            class="text-center w-44 pt-10 inline ml-10"
            alt="date"
        />
        <p
            class="align-bottom inline text-5xl font-bold italic text-slate-400 -ml-3"
        >
            {traduction.salon_preso_title}
        </p>
        <SalonMode />
    </div>

    <div
        class="w-3/4 border-b-4 border-salte-200 text-center mx-auto mb-20 mt-10"
    />
    <div id="#anchor-id">
        <img
            src="/id3.svg"
            class="text-center w-44 pt-10 inline ml-10"
            alt="date"
        />
        <p
            class="align-bottom inline text-5xl font-bold italic text-slate-400 -ml-3"
        >
            {traduction.company_preso_title}
        </p>
        <ID />
    </div>
    <div
        class="w-3/4 border-b-4 border-salte-200 text-center mx-auto mb-20 mt-10"
    />
    <div id="#anchor-form">
        <img
            src="/id3.svg"
            class="text-center w-44 pt-10 inline ml-10"
            alt="date"
        />
        <p
            class="align-bottom inline text-5xl font-bold italic text-slate-400 -ml-3"
        >
            {traduction.titlte_perso_forms}
        </p>
        <Form />
    </div>
    <div
        class="w-3/4 border-b-4 border-salte-200 text-center mx-auto mb-20 mt-10"
    />
    <div id="#anchor-requested">
        <img
            src="/form.svg"
            class="text-center w-44 pt-10 inline ml-10"
            alt="date"
        />
        <p
            class="align-bottom inline text-5xl font-bold italic text-slate-400 -ml-3"
        >
            {traduction.required_preso_title}
        </p>
        <Requested />
    </div>
    <div
        class="w-3/4 border-b-4 border-salte-200 text-center mx-auto mb-20 mt-10"
    />
    <div id="#anchor-extras">
        <img
            src="/extra2.svg"
            class="text-center w-44 pt-10 inline ml-10"
            alt="date"
        />
        <p
            class="align-bottom inline text-5xl font-bold italic text-slate-400 -ml-3"
        >
            {traduction.extra_preso_title}
        </p>
        <ExtraRequesteds />
    </div>
    <div
        class="w-3/4 border-b-4 border-salte-200 text-center mx-auto mb-20 mt-10"
    />
    <!-- <div id="#anchor-socials">
            <p class="text-4xl pt-10 ml-8 text-slate-500 ">
                {traduction.socials_preso_title}
            </p>
            <Socials />
        </div> -->
</section>

<style>
    section {
        z-index: 99;
    }
</style>
