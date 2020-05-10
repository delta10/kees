<template>
  <div class="alert alert-dismissible fade show" :class="`alert-${type}`" role="alert">
    {{ message }}
  </div>
</template>

<script>
export default {
  name: 'Alert',
  props: {
    type: { type: String, default: 'success' },
    message: String
  },
}
</script>