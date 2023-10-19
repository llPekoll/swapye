<script lang="ts">
    export let valueToSet = false;
    export let name = "";
    export let tradsToDisp = "";
    export let needsUpdate = false;
    export let disabled = false;
</script>

<div class="clear-both py-2">
    <label class="toggler-wrapper style-1 float-right">
        <input
            on:click={() => (needsUpdate = true)}
            on:keypress={() => (needsUpdate = true)}
            type="checkbox"
            {name}
            {disabled}
            bind:checked={valueToSet}
        />
        <div class="toggler-slider">
            <div class="toggler-knob" />
        </div>
    </label>
    <p class="text-slate-600">{tradsToDisp}</p>
</div>

<style>
    input[type="checkbox"] {
        position: absolute;
        opacity: 0;
        z-index: -1;
    }

    .toggler-wrapper.style-1
        input[type="checkbox"]:checked
        + .toggler-slider
        .toggler-knob {
        left: calc(100% - 19px - 3px);
    }

    .toggler-wrapper.style-1 .toggler-knob {
        width: calc(25px - 6px);
        height: calc(25px - 6px);
        border-radius: 50%;
        left: 3px;
        top: 3px;
        background-color: #fff;
    }
    @charset "UTF-8";
    .toggler-wrapper {
        display: block;
        width: 45px;
        height: 25px;
        cursor: pointer;
        position: relative;
    }

    .toggler-wrapper input[type="checkbox"] {
        display: none;
    }

    .toggler-wrapper input[type="checkbox"]:checked + .toggler-slider {
        background-color: #44cc66;
    }

    .toggler-wrapper .toggler-slider {
        background-color: #ccc;
        position: absolute;
        border-radius: 100px;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        -webkit-transition: all 300ms ease;
        transition: all 300ms ease;
    }

    .toggler-wrapper .toggler-knob {
        position: absolute;
        -webkit-transition: all 300ms ease;
        transition: all 300ms ease;
    }
</style>
