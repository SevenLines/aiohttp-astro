<template>
  <g class="aspect" v-if="type != 'conjunction'">
    <circle :cx="start.x" :cy="start.y" r="5"></circle>
    <circle :cx="end.x" :cy="end.y" r="5"></circle>
    <path class :d="path"></path>
    <path :d="path" class="sub-path" @mouseover="onHover"></path>
    <path :d="path" class="main-path" @mouseover="onHover"></path>


    <rect v-if="type==='square'" :x="center.x - 5" :y="center.y - 5" width="10" height="10"></rect>
    <polygon v-if="type==='trine'" :points="trinePoints"></polygon>
  </g>
</template>


<script>
  export default {
    name: 'aspect',
    props: ['planet1', 'planet2', 'type', 'width', 'circleWidth'],
    mounted () {
    },
    computed: {
      trinePoints () {
        return `${this.center.x - 7},${this.center.y + 7} ` +
          `${this.center.x},${this.center.y - 7} ` +
          `${this.center.x + 7},${this.center.y + 7}`
      },
      title () {
        return `${this.type} | ${this.planet1.name} - ${this.planet2.name}`
      },
      length () {
        return this.width / 2 - this.circleWidth
      },
      center () {
        return {
          x: (this.start.x + this.end.x) / 2,
          y: (this.start.y + this.end.y) / 2
        }
      },
      start () {
        let angle = Math.degrees(this.planet1.lon)
        return {
          x: Math.cos(Math.radians(-angle)) * this.length,
          y: Math.sin(Math.radians(-angle)) * this.length
        }
      },
      end () {
        let angle = Math.degrees(this.planet2.lon)
        return {
          x: Math.cos(Math.radians(-angle)) * this.length,
          y: Math.sin(Math.radians(-angle)) * this.length
        }
      },
      path () {
        return `M${this.start.x} ${this.start.y} L${this.end.x} ${this.end.y}`
      }
    },
    methods: {
      onHover () {
        this.$emit('aspectHover')
      }
    }
  }
</script>

<style lang="scss" scoped="">
  .aspect {
    path, circle {
      cursor: pointer;
      stroke: black;
      stroke-width: 1px;

      -webkit-transition: all 0.2s;
      -moz-transition: all 0.2s;
      -ms-transition: all 0.2s;
      -o-transition: all 0.2s;
      transition: all 0.2s;

    }

    .sub-path {
      stroke-width: 16;
      stroke: rgba(0, 0, 0, 0);
    }

    text {
      text-anchor: middle;
      dominant-baseline: middle;
      visibility: hidden;
    }

    &:hover {
      path.main-path, circle, polygon, rect {
        $color: #ffca00;
        fill: $color;
        stroke-width: 2px;
        stroke: $color;
      }
      text {
        visibility: visible;
      }
    }
  }
</style>
