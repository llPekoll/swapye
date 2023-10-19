<script lang="ts">
    export let name = "";
    export let val = "";
    export let inputName = "";
    export let needsUpdate = false;
</script>

<label class="block text-gray-500 font-bold mb-1 pr-4" for="inline-full-name">
    {name}
</label>
<div class="md:w-2/3 ml-4">
    <input
        type="text"
        name={inputName}
        class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
        bind:value={val}
        on:blur={() => (needsUpdate = true)}
    />
</div>
