<template>
  <v-navigation-drawer app clipped :mini-variant="isMin">
    <v-list nav>
      <v-list-item-group active-class="primary--text text--accent-4">
        <v-list-item v-for="(link, i) in links" :key="i" link :to="link.route">
          <v-list-item-icon>
            <v-icon>{{ link.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ link.title }}</v-list-item-title>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>
<script>
export default {
  props: {
    isMin: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      links: [
        {
          title: "Home",
          icon: "mdi-home",
          route: "/home",
        },
        {
          title: "Settings",
          icon: "mdi-cog",
          route: "/settings",
        },
      ],
    };
  },
};
</script>
