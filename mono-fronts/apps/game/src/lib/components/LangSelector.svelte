<script lang="ts">
    import {
        Menu,
        MenuButton,
        MenuItems,
        MenuItem,
    } from "@rgossiaux/svelte-headlessui";
    export let lang = "";
    export let langs: string[] = [];
    let disp = lang.substring(0, 7).toUpperCase();
</script>

<Menu
    class="w-22 fixed md:right-20 md:top-20 md:scale-100 top-1 right-1 scale-75"
>
    <MenuButton class="headlessui-menu-button">
        {disp}
        <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            aria-hidden="true"
            class="w-5 h-5 ml-2 -mr-1 text-violet-200 hover:text-violet-100"
            ><path
                fill-rule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clip-rule="evenodd"
            /></svg
        >
    </MenuButton>
    <MenuItems class="headlessui-menu-items">
        {#each langs as langItem}
            <MenuItem
                let:active
                class="headlessui-menu-item"
                on:click={() => {
                    disp = langItem.substring(0, 7).toUpperCase();
                    lang = langItem;
                }}
            >
                {langItem}
            </MenuItem>
        {/each}
    </MenuItems>
</Menu>

<style lang="postcss">
    :global(.headlessui-menu-button) {
        @apply inline-flex justify-center  px-4 py-2 text-sm font-medium text-white bg-black rounded-md bg-opacity-20 hover:bg-opacity-30 focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75;
    }
    :global(.headlessui-menu-items) {
        @apply absolute right-0 w-56 mt-2 origin-top-right bg-white divide-y divide-gray-100 rounded-md shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none p-2;
    }
    :global(.headlessui-menu-item) {
        @apply text-gray-900 flex rounded-md items-center w-full px-2 py-2 text-sm hover:bg-gray-100;
    }
</style>
