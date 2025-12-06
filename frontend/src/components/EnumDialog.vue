<template>
  <Dialog v-model:visible="visible" header="Enumeration Values">
    <table class="grouped" v-for="e in data" :key="e.value">
      <tr>
        <td class="pr-2 pb-2">{{ e.value }}</td>
        <td class="pr-2 pb-2">{{ e.definition }}</td>
        <td v-if="e.comment" class="pb-2 text.xs font-light">
          {{ e.comment }}
        </td>
      </tr>
    </table>
  </Dialog>
</template>

<script>
export default {
  name: 'EnumDialog',
  props: {
    data: Array
  },
  data() {
    return {
      visible: false
    };
  },
  methods: {
    setVisible(visible) {
      this.visible = visible;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
table.grouped {
  display: table-row-group;
}
</style>
