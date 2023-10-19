<script lang="ts">
    import { emblem } from "$lib/stores/index";
    import { page } from "$app/stores";
    export let qr_location = "";
    export let link = "";

    const traduction = $page.data.user.traduction;
    const deleteGame = (e: Event) => {
        if (confirm("Etes vous sure de vouloir supprimer ce jeux?")) {
            const target = e.currentTarget as HTMLFormElement;
            target.submit();
        }
    };
</script>

<svelte:head>
    <title>{traduction.title_game_info}</title>
</svelte:head>
<section class="p-10 ">
    <div>
        <img
            src="/diffusion.svg"
            class="text-center w-44 pt-10 inline "
            alt="date"
        />
        <p
            class="align-bottom inline text-5xl font-bold italic text-slate-400 "
        >
            {traduction.menu_game_info}
        </p>
    </div>
    <div class="text-center mx-auto mt-10">
        <p>
            <img
                src={qr_location}
                alt="qr code"
                class="w-44 text-center mx-auto mb-5 shadow-lg rounded-lg"
            />
        </p>
        <!-- svelte-ignore security-anchor-rel-noreferrer -->
        <a href={link} target="_blank">
            {link}
        </a>
    </div>
</section>
<form
    on:submit|preventDefault={deleteGame}
    class="text-center pt-10"
    method="POST"
    action="?/deleteGame"
>
    <input type="hidden" name="emblem" value={$emblem} />
    <button type="submit" class="bg-red-500 px-10 py-2 rounded-lg text-white">
        {traduction.info_delete_game}
    </button>
</form>
