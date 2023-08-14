<template>
<div class="user-data">
    <div><h2>Please Enter Your Data</h2></div>
    <div class="location">
        <label for="location">Location:&nbsp;</label>
        <input type="text" id="location" v-model="location" placeholder="Enter Location" class="location-input">
    </div>

    <div class="age">
    <label for="age">Age:&nbsp;</label>
    <input type="number" id="age" v-model.number="age" class="age-input">
    </div>

    <div class="gender">
    <label for="gender">Gender:&nbsp;</label>
    <select id="gender" v-model="gender" class="select-gender">
    <option value="Male">Male</option>
    <option value="Female">Female</option>
    <option value="Unisex">Unisex</option>
    </select>
    </div>

    <div class="wrapCount">
        <div class="productCount">
        <div class="productLabel"><label for="productCount">Number of Products:&nbsp;</label></div>
        <div class="productInput"><input type="range" id="productCount" v-model="productCount" min="1" max="99"></div>
        <div class="productValue"><span>&nbsp;{{ formattedSelectedValue }}</span></div>
        </div>
    </div>

    <div>
        <div class="similarity-box">
            <div class="productLabel"><label for="trendy">More Trendy&nbsp;</label></div>
            <div class="productInput"><input type="range" id="similarity" v-model="similarity" step="0.01" min="0.5" max="0.8"></div>
            <div class="productLabel"><label for="exact">&nbsp;More Exact</label></div>
        </div>
    </div>

    <button @click="submitForm">Submit</button>
</div>
</template>
  
<script>
export default {
    data() {
        return {
            location: '',
            productCount:1,
            age:0,
            gender:'',
            similarity:0.5
        }
    },
    methods: {
        submitForm() {
            //To do
            // Send axios request to backend
            console.log(this.location,this.productCount,this.age,this.gender,this.similarity)
        }
    },
    computed: {
        formattedSelectedValue() {
          return String(this.productCount).padStart(2, '0');
        }
      }
}
</script>

<style>
    .similarity-box{
        padding:1vh 6.6vh 1vh 6.6vh;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content:space-evenly;
        border: 1px solid silver;
    }

    .user-data{
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        align-items: center;
        font-family:  'Roboto', sans-serif;
        gap:1%      
    }

    .location-input{
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 16px;
        box-sizing: border-box;
        resize: horizontal;
        font-family:  'Roboto', sans-serif;
    } 

    .location{
        border: 1px solid silver;
        padding:1vh 10vh 1vh 10vh;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }

    .gender{
        border: 1px solid silver;
        padding:1vh 18.1vh 1vh 18.1vh;
    }

    .age{
        border: 1px solid silver;
        padding:1vh 12.2vh 1vh 12.2vh;;
    }

    .age-input{
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 16px;
        box-sizing: border-box;
        resize: horizontal;
        font-family:  'Roboto', sans-serif;
    }

    .productCount{
        border: 1px solid silver;
        padding:1vh 7vh 1vh 7vh;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content:space-evenly;
    }

    .select-gender{
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 16px;
        box-sizing: border-box;
        resize: horizontal;
        font-family:  'Roboto', sans-serif;
    }

</style>