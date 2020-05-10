<template>
  <div>
    <h5>{{field.label}}</h5>
    <hr />
  </div>
</template>

<script>
export default {
  name: 'Heading',
  props: {
    field: Object
  }
}
</script>