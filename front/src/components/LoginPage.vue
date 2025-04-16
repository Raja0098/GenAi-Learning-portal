<template>
  
<!--
  <div class="row justify-content-center">
  <div class="row row-cols-1">
  <form @submit.prevent="login">
    Email ID: <input type="text" v-model="username" placeholder="Username" /><br /><br />
    Password : <input type="password" v-model="password" placeholder="Password" />
    <button id="submit" type="submit">Login</button>
  </form>
  </div>
  </div>
-->
<div class="main ms-4 me-4">
  <div :class="alert.type" class="alert alert-dismissible fade show text-center" role="alert" v-if="alert.type">
    <strong>Attention : </strong> {{ message }}
    <button type="button" @click="closeAlert" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  </div>
    <div class="row">
      <div id="login_page" class="col-12 justify-content-center d-flex align-items-center mt-3" align="right">
      <!-- begin login form -->
        <div id="login" align="center" v-if="login">
                <div class="card mb-3">
                <div class="card-header" style="background-color:#99503e7d;"><p class="text-start fs-5 m-0">Sign in</p></div>
                  <div class="card-body">
                    <form id="login_form" action="" method="post" class="needs-validation">
                      <!-- Email input -->
                      
                      <div class="form-floating mb-4 has-validation">
                        <input type="text" id="l_e" name="email" class="form-control ms-0 border border-secondary" placeholder="email" v-model="username" v-bind:class="{ 'is-invalid': error.email }" required />
                        <label class="form-label fs-6" id="l_p" for="email" >Email</label>
                        <div class="invalid-feedback" v-if="error.email">
                      {{ error.email }}
              </div>
              <div class="invalid-feedback" v-else>
                      Invalid Email.
              </div>
                      </div>
                      <!-- Password input -->
                      <div class="form-floating mb-4 has-validation">
                        <input type="password" name="password" class="form-control ms-0 border border-secondary" placeholder="password" v-model="password" v-bind:class="{ 'is-invalid': error.password }" required />
                        <label class="form-label fs-6" for="password" >Password</label>
                        <div class="invalid-feedback" v-if="error.email">
                      {{ error.email }}
              </div>
              <div class="invalid-feedback" v-else>
                      Please provide password.
              </div>
                      </div>
                      <p class="warning text-danger fs-6" v-if="message">*&nbsp;{{ message }}&nbsp;*</p>
                      <!-- Submit button -->
                      <button type="submit" @click.prevent="checkForm('login_form')" class="btn btn-block fs-6 text-end" style="
    background: #8d4a3a;
    color: antiquewhite;">Sign in</button>
                      <br>
                      <!--
                      <p class="text-muted fs-4">Don't have an account ?
                      <a id="register_link" href="#" @click.prevent="switch_form('signup')">Register</a></p>
                      -->
                    </form>
                </div>
              </div>
            </div>
        <!-- end login form  -->


      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
      message: '',
      alert:'',
      error:'',
      formData:'',
    }
  },

  methods: {

    checkForm(id){

      this.message = ''
    
      var form = document.getElementById(id)
      var elems = form.getElementsByTagName("input")


        Array.prototype.slice.call(elems).forEach(function (form) {
        if(!form.checkValidity()){

              form.classList.add('is-invalid')
              //console.log("is-invalid")
        }
            else{   
              //console.log("is-valid")
              form.classList.remove('is-invalid')
              form.classList.add('is-valid')
            }       
            
        })

        if(form.checkValidity()){
        if (id == "login_form")
            this.login()
          //if (id == "register_form")
          //  this.registerUser()
        }

      },

    async login() {

      const response = await fetch('http://127.0.0.1:5000/api/studentLogin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password
        })
      })
      const data = await response.json()
      if (response.ok) {
        const user_id = data['user_id']
        this.$store.commit('setCurrentUser', { id: data['user_id'], name: data['user_name']})
        //console.log(this.$store.state.current_user.id)
        this.$router.push({ path: '/studentDashboard', query: { user_id } })
      } else {

        this.message = data['message']
        //console.log(this.message)

        var form = document.getElementById('login_form')
        var elems = form.getElementsByTagName("input")


        Array.prototype.slice.call(elems).forEach(function (form) {
              form.classList.remove('is-invalid') //remove the highlighting
              form.classList.remove('is-valid') //remove the highlighting
        })
        
      }
    }
  }
}
</script>

<style scoped>
form {
  font-size: 20px;
  width: 100%;
  align-items: center;
  justify-content: center;
}

fieldset {
  width: fit-content;
  margin: 0 auto;
  width: fit-content;
  padding-top: 40%;
  padding-bottom: 45%;
  font-size: 20px;
  align-items: center;
  justify-content: center;
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial,
    sans-serif;
  border: none;
}

legend {
  width: fit-content;
  padding: 3px;
  font-size: 27px;
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial,
    sans-serif;
  font-weight: bold;
}

input {
  display: inline-block;
  border: none;
  font-size: 25px;
  margin-left: 20px;
  outline: none;
}

#submit {
  border-radius: 0.2em;
  font-size: 100%;
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial,
    sans-serif;
  font-weight: bolder;
  padding: 3%;
  margin-left: 40%;
  margin-top: 10%;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: fit-content;
  cursor: pointer;
  background-color: #8d493a;
  border: none;
}
</style>
