<script lang="ts">
    import Form from "$lib/components/Form.svelte";
    export let data;
    const trads = data.trads;
    const lang: string = data.langs[0] as string;
    let fullScreenSwitcher: () => void = function jose() {
        console.log("fullScreenSwitcher");
    };
</script>

<section class="w-full h-full">
    <Form {lang} {trads} {fullScreenSwitcher} />
</section>
