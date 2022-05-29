<template>
    <ModalLayout :desc="desc" :symbol="symbol" :buttonCode="buttonCode"/>
</template>

<script>
  import ModalLayout from './Modal_layout';
  
  export default {
    name: 'Info',
    components: {
        ModalLayout
    },
    data: function () {
        return {
            desc: '',
            symbol: '',
            buttonCode: ''
        }
    },
    created () {
        this.desc = this.$router.history.current.query.desc

        if(this.desc == 'Acerca de'){
            this.symbol = 'fa fa-info-circle'
            this.buttonCode = '2.1'
        }
        else if (this.desc == 'Créditos'){
            this.symbol = 'fa fa-users'
            this.buttonCode = '4.1'
        }
        else if (this.desc == 'Termos de utilização'){
            this.symbol = 'fa fa-address-book'
            this.buttonCode = '3.1'
        }
        else if (this.desc == 'Privacidade'){
            this.symbol = 'fa fa-lock'
            this.buttonCode = '5.1'
        }
    }
  }
</script>
