<script lang="ts">
    import NavElement from "./NavElement.svelte";
    import { page } from "$app/stores";
    import { applyAction, enhance } from "$app/forms";
    import { invalidateAll } from "$app/navigation";

    export let email = "";
    const traduction = $page.data.user.traduction;
    let gameEdition = false;
    $: if (
        $page.url.pathname.split("/")[1] === "games" &&
        $page.url.pathname.split("/").length === 3
    ) {
        gameEdition = true;
    } else {
        gameEdition = false;
    }
    const dataIcon = `<svg width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" d="M21 5.662v.676c0 1.734 1.365 1.661 1.5 1.661c.146 0 1.5.083 1.5-1.661v-.676c0-1.734-1.365-1.661-1.5-1.661c-.146 0-1.5-.083-1.5 1.661Zm2.125-.11v.886c0 .703-.219.94-.615.94s-.625-.237-.625-.94v-.885c0-.685.23-.922.615-.922c.396-.01.625.237.625.922ZM21 12.662v.676c0 1.734 1.365 1.661 1.5 1.661c.146 0 1.5.083 1.5-1.661v-.676c0-1.734-1.365-1.661-1.5-1.661c-.146 0-1.5-.083-1.5 1.661Zm2.125-.11v.886c0 .703-.219.94-.615.94s-.625-.237-.625-.94v-.885c0-.685.23-.922.615-.922c.396-.01.625.237.625.922ZM21 19.662v.676c0 1.734 1.365 1.661 1.5 1.661c.146 0 1.5.083 1.5-1.661v-.676c0-1.734-1.365-1.661-1.5-1.661c-.146 0-1.5-.083-1.5 1.661Zm2.125-.11v.886c0 .703-.219.94-.615.94s-.625-.237-.625-.94v-.885c0-.685.23-.922.615-.922c.396-.01.625.237.625.922ZM17 9.662v.676c0 1.734 1.365 1.661 1.5 1.661c.146 0 1.5.083 1.5-1.661v-.676c0-1.734-1.365-1.661-1.5-1.661c-.146 0-1.5-.083-1.5 1.661Zm2.125-.11v.886c0 .703-.219.94-.615.94s-.625-.237-.625-.94v-.885c0-.685.23-.922.615-.922c.396-.01.625.237.625.922ZM17 1.59v.647l1-.238V5h1V1m-2 14.59v.647l1-.238V19h1.001v-4M16 21v3H0v-3c0-2.66 5.33-4 8-4s8 1.34 8 4Z"></path><circle cx="8" cy="12" r="4" fill="currentColor"></circle><path fill="currentColor" d="M17.885 23.553c0-.685.23-.922.615-.922c.396-.01.625.237.625.922V24H20v-.338c0-1.734-1.365-1.661-1.5-1.661c-.146 0-1.5-.083-1.5 1.661V24h.885Z"></path></svg>`;
    const gamesIcon = `<svg width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" d="M12 22c3.719 0 7.063-2.035 8.809-5.314L13 12l7.809-4.686C19.063 4.035 15.719 2 12 2C6.486 2 2 6.486 2 12s4.486 10 10 10zm-.5-16a1.5 1.5 0 1 1-.001 3.001A1.5 1.5 0 0 1 11.5 6z"></path></svg>`;
    const settingsIcon = `<svg width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" d="m18.525 9l-1.1-2.4l-2.4-1.1l2.4-1.1l1.1-2.4l1.1 2.4l2.4 1.1l-2.4 1.1Zm2 7l-.8-1.7l-1.7-.8l1.7-.8l.8-1.7l.8 1.7l1.7.8l-1.7.8Zm-13 6l-.3-2.35q-.2-.075-.387-.2q-.188-.125-.313-.25l-2.2.95l-2.5-4.35l1.9-1.4v-.8l-1.9-1.4l2.5-4.35l2.2.95q.125-.125.313-.25q.187-.125.387-.2l.3-2.35h5l.3 2.35q.2.075.388.2q.187.125.312.25l2.2-.95l2.5 4.35l-1.9 1.4v.8l1.9 1.4l-2.5 4.35l-2.2-.95q-.125.125-.312.25q-.188.125-.388.2l-.3 2.35Zm2.5-5q1.25 0 2.125-.875T13.025 14q0-1.25-.875-2.125T10.025 11q-1.25 0-2.125.875T7.025 14q0 1.25.875 2.125t2.125.875Z"></path></svg>`;
</script>

<section class="md:grid-cols-none grid grid-cols-4 text-white">
    <div
        class="on-top fixed bg-bleu-gris left-0
    {gameEdition ? 'md:w-20' : 'md:w-44'}  md:h-full md:text-left md:pl-5
    w-full bottom-0 h-20 text-center shadow-md rounded-tr-3xl
      "
    >
        <div class="flex pt-7 text-center mx-auto pb-10">
            <img
                src={traduction.logo_swapye_couleur}
                alt="logo"
                class="w-4 scale-150 mr-4 ml-2"
            />
            {#if !gameEdition}
                <h1 class="hidden md:block font-bold ">
                    {traduction.name}
                </h1>
            {/if}
        </div>

        <ul
            class="md:pl-0 pl-10 md:grid-cols-none grid grid-cols-2 w-3/5 md:w-full md:text-left text-center mx-auto pt-3"
        >
            <NavElement
                icon={gamesIcon}
                title="Games"
                link="/games"
                {gameEdition}
            />
            <NavElement
                icon={dataIcon}
                title="Data"
                link="/data"
                {gameEdition}
            />
            <NavElement
                icon={settingsIcon}
                title="Settings"
                link="/settings"
                {gameEdition}
            />
        </ul>
        {#if !gameEdition}
            <div
                class="text-center absolute bottom-6 right-0 md:left-0 md:w-full"
            >
                <form
                    action="/logout"
                    method="POST"
                    use:enhance={() => {
                        return async ({ result }) => {
                            invalidateAll();
                            await applyAction(result);
                        };
                    }}
                >
                    <button
                        type="submit"
                        title="logout"
                        class="md:inline hidden bg-new-orange rounded-xl py-2 px-10 font-bold shadow-lg shadow-new-orange/50"
                    >
                        {traduction.logout}
                    </button>
                </form>
                <p class="text-xs pt-3">
                    {email}
                </p>
            </div>
        {/if}
    </div>
</section>
