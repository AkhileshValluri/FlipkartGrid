<template>
  <div class="user-data">
    <div class="heading">
      <h3><u>Please Enter Your Data</u></h3>
    </div>
    <div class="location">
      <div class="location2">
        <label for="location">Location:&nbsp;</label>
        <input
          type="text"
          id="location"
          v-model="formData.location"
          placeholder="Enter Your Location"
          class="location-input"
        />
      </div>
    </div>

    <div class="age">
      <div class="age2">
        <label for="age">Age:&nbsp;</label>
        <input
          type="number"
          id="age"
          v-model.number="formData.age"
          class="age-input"
          min="1"
          max="99"
        />
      </div>
    </div>

    <div class="gender">
      <div class="gender2">
        <label for="gender">Gender:&nbsp;</label>
        <select id="gender" v-model="formData.gender" class="select-gender">
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Unisex">Unisex</option>
        </select>
      </div>
    </div>

    <div class="productCount">
      <div class="productCount2">
        <div class="productLabel">
          <label for="productCount">Number of Products:&nbsp; Less </label>
        </div>
        <div class="productInput">
          <input
            type="range"
            id="productCount"
            v-model="formData.productCount"
            min="1"
            max="99"
          />
        </div>
        <div class="productLabel">More</div>
      </div>
    </div>

    <div class="similarity-box">
      <div class="similarity-box2">
        <div class="productLabel">
          <label for="trendy">More Trendy&nbsp;</label>
        </div>
        <div class="productInput">
          <input
            type="range"
            id="trendy"
            v-model="formData.similarity"
            step="0.01"
            min="0.5"
            max="0.8"
          />
        </div>
        <div class="productLabel">
          <label for="exact">&nbsp;More Exact</label>
        </div>
      </div>
    </div>

    <div class="image-upload-box">
      <div class="image-upload-box2">
        <div><label for="image" class="productLabel">Image</label></div>
        <div>
          <input
            type="file"
            name="image"
            accept="image/jpeg"
            class="imageInput"
          />
        </div>
      </div>
    </div>

    <button @click="submitForm" :class="[isSubmit ? 'submit' : 'submitted']">
      {{ submit }}
    </button>
  </div>
</template>

<script>

export default {
  data() {
    return {
      formData:{
          location: "",
          productCount: 1,
          age: 1,
          gender: "",
          similarity: 0.5,
      },
      submit: "Submit",
      isSubmit: true,
    };
  },
  methods: {
    submitForm() {
      this.$emit('form-submitted',this.formData);
      this.isSubmit = false;
      if (!this.isSubmit && this.submit === "Submitted") {
        window.alert(
          "Already submitted user data, please refresh to enter new user data"
        );
        return;
      }
      this.submit = "Submitted";
      console.log(
        this.formData.location,
        this.formData.productCount,
        this.formData.age,
        this.formData.gender,
        this.formData.similarity
      );
    },
  },
};
</script>

<style>
.submit {
  margin-bottom: 2%;
}

.submitted {
  margin-bottom: 2%;
  background-color: yellowgreen;
}

.imageInput {
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  box-sizing: border-box;
  resize: horizontal;
  font-family: "Roboto", sans-serif;
}

.heading {
  width: 99%;
  text-align: center;
}

.image-upload-box2 {
  padding: 0.5vh 0vh 0.5vh 0vh;
  display: flex;
  width: 99%;
  flex-direction: row;
  align-items: center;
  justify-content: space-evenly;
}

.image-upload-box {
  border-radius: 5px;
  display: flex;
  width: 99%;
  flex-direction: row;
  align-items: center;
  border: 1px solid silver;
}

.similarity-box2 {
  padding: 0.5vh 0vh 0.5vh 0vh;
  display: flex;
  width: 100%;
  flex-direction: row;
  align-items: center;
  justify-content: space-evenly;
}

.similarity-box {
  border-radius: 5px;
  display: flex;
  width: 99%;
  flex-direction: row;
  align-items: center;
  border: 1px solid silver;
}

.user-data {
  font-size: 16px;
  width: 100%;
  height: 100%;
  border: 1px solid silver;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  font-family: "Roboto", sans-serif;
  gap: 1vh;
}

.location-input {
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  box-sizing: border-box;
  resize: horizontal;
  font-family: "Roboto", sans-serif;
}

.location2 {
  padding: 0.5vh 0vh 0.5vh 0vh;
  display: flex;
  width: 100%;
  flex-direction: row;
  align-items: center;
  justify-content: space-evenly;
}

.location {
  border-radius: 5px;
  display: flex;
  width: 99%;
  flex-direction: row;
  align-items: center;
  border: 1px solid silver;
}

.gender2 {
  padding: 0.5vh 0vh 0.5vh 0vh;
  display: flex;
  width: 100%;
  flex-direction: row;
  align-items: center;
  justify-content: space-evenly;
}

.gender {
  border-radius: 5px;
  display: flex;
  width: 99%;
  flex-direction: row;
  align-items: center;
  border: 1px solid silver;
}

.age2 {
  padding: 0.5vh 0vh 0.5vh 0vh;
  display: flex;
  width: 100%;
  flex-direction: row;
  align-items: center;
  justify-content: space-evenly;
}

.age {
  border-radius: 5px;
  display: flex;
  width: 99%;
  flex-direction: row;
  align-items: center;
  border: 1px solid silver;
}

.age-input {
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  box-sizing: border-box;
  resize: horizontal;
  font-family: "Roboto", sans-serif;
}

.productCount {
  border-radius: 5px;
  border: 1px solid silver;
  display: flex;
  flex-direction: row;
  width: 99%;
}

.productCount2 {
  padding: 0.5vh 0vh 0.5vh 0vh;
  display: flex;
  width: 99%;
  flex-direction: row;
  align-items: center;
  justify-content: space-evenly;
}

.select-gender {
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  box-sizing: border-box;
  resize: horizontal;
  font-family: "Roboto", sans-serif;
}

 .productInput{
  background-color: #ffdd00;
  border-radius: 5px;
 }

</style>
