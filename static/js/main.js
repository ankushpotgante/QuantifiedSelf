
const Login = Vue.component('Login', {
    data: function () {
        return {
            username: '',
            passwd: '',
            access_token: '',
            problem: false,
            message: "",
        }
    },
    template:
        `
    <div>
        <div class="container text-center" style="margin-top: 10px">
            <h1>Quantified Self</h1>
            <p>track and measure yourself!</p>
        </div>

        <div class="d-flex justify-content-center" style="margin-top:7%; position: relative;">
            <br>
            <div class="row" style="border:1px solid grey; padding: 2%;">
            
                <div>
                    <h2>Login</h2>
                    <br>
                    <div v-if="message" class="row">
                        <p class="alert alert-warning" role="alert">{{ message }}</p>
                        <br>
                    </div>
                    <div class="mb-3">
                        <label for="username" class="form-label">Username </label>
                        <input type="text" v-model="username" class="form-control" id="username" name="username" required>
                    </div>

                    <div class="mb-3">
                        <label for="passwd" class="form-label">Password </label>
                        <input type="password" v-model="passwd" class="form-control" id="passwd" name="passwd" required>
                    </div>
                        <input type="button" @click="sign_in" class="btn btn-primary" value="Login">
                    <p>Don't have an account, <router-link to="/register">click here</router-link> to register</p>
                </div>
            </div>
        </div>
    </div>
    `,

    methods: {
        'sign_in': function () {

            this.message = "";

            fetch("http://127.0.0.1:5000/api/login", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    //'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: JSON.stringify({ "username": this.username, "password": this.passwd })
            }).then((response) => {
                return response.json()
            })
                .then((data) => {
                    if (data.access_token) {
                        this.access_token = data.access_token;
                        console.log("Got access token");
                        localStorage.access_token = data.access_token;
                        localStorage.fname = data.first_name;
                        localStorage.uid = data.uid;
                        this.$emit('set_data');
                        router.push({ path: '/', params: { uid: data.uid } });

                    } else {
                        console.log(data);
                        //this.message = data.message;

                    }
                }).catch(error => { console.error("Error: ", error) });

        }
    }
})


const Register = Vue.component('Register', {
    data: function () {
        return {
            fname: '',
            lname: '',
            email: '',
            uname: '',
            passwd: '',
            message: ''
        }
    },

    template:

        `
    <div>
        <div class="container text-center" style="margin-top: 10px;">
            <h1>Quantified Self</h1>
            <p>track and measure yourself!</p>
        </div>

        <div class="d-flex justify-content-center" style="margin-top:1%; position: relative;">
            <br>
            <div class="row" style="border:1px solid grey; padding: 2%;">
                <div>
                    <h2>Register</h2>
                    <br>
                    
                    <div v-if="message" class="row">
                        <p class="alert alert-warning" role="alert">{{ message }}</p>
                        <br>
                    </div>

                    <div class="mb-3">
                        <label for="fname" class="form-label">First Name </label>
                        <input type="text" v-model="fname" class="form-control" id="fname" name="fname" required>
                    </div>

                    <div class="mb-3">
                        <label for="lname" class="form-label">Last Name </label>
                        <input type="text" v-model="lname" class="form-control" id="lname" name="lname" required>
                    </div>


                    <div class="mb-3">
                        <label for="email" class="form-label">Email </label>
                        <input type="email" v-model="email" class="form-control" id="email" name="email" required>
                    </div>


                    <div class="mb-3">
                        <label for="uname" class="form-label">Username </label>
                        <input type="text" v-model="uname" class="form-control" id="uname" name="uname" required>
                    </div>

                    <div class="mb-3">
                        <label for="passwd" class="form-label">Password </label>
                        <input type="password" v-model="passwd" class="form-control" id="passwd" name="passwd" required>
                    </div>

                        <input type="button" @click="register" class="btn btn-primary" value="Register">
                    
                    <p>Already have an account, <router-link to="/login">click here</router-link> to login</p>
                </div>
            </div>
        </div>
    </div>

    `,

    methods: {
        'register': function () {
            this.message = "";

            fetch("http://127.0.0.1:5000/api/user", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    //'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: JSON.stringify({ "first_name": this.fname, "last_name": this.lname, "email": this.email, "username": this.uname, "password": this.passwd })
            }).then((response) => {
                if (response.status == 201) {
                    console.log("successfully created user!!")
                }
                return response.json()
            })
                .then((data) => {
                    //console.log(data);
                    this.message = data.message;
                    router.push({ path: '/login' })
                }).catch(error => { console.error("Error: ", error) });
        }
    }
})


const Index = Vue.component('Index', {

    props: ['uid'],

    data: function () {
        return {
            trackers: '',
            message: '',
        }
    },

    template:
        `
    <div class="d-flex justify-content-center" style="margin-top:7%; position: relative;">
        <div class="row" style="padding: 2%;">
            <div>
                <table class="table text-center">
                    <thead>
                        <tr>
                            <th>Tracker</th>
                            <th>Last tracked</th>
                            <th></th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                    
                    <tr v-for="(t, index) in trackers">
                        <td>
                            <router-link :to="{path:'/tracker/' + t.tid }">{{ t.name }}</router-link>
                        </td>

                        <td> {{ t.last_tracked }} </td>

                        <td>
                            <router-link :to="{path: '/tracker/' + t.tid + '/log'}">
                                <!-- svg image for log -->
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                    class="bi bi-plus-lg" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd"
                                        d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z"/>
                                </svg>
                            </router-link>
                        </td>
                        <td>
                            <router-link :to="{path: '/edit_tracker/' + t.tid}" class="link-success">
                                <!-- svg image for edit -->
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                    class="bi bi-pencil-square" viewBox="0 0 16 16">
                                    <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                    <path fill-rule="evenodd"
                                        d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
                                </svg>
                            </router-link>
                            &nbsp; &nbsp;
                            <a href="#" @click="delete_tracker(t.tid, index)" class="link-danger">
                                <!-- svg image for delete -->
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                    class="bi bi-trash" viewBox="0 0 16 16">
                                    <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                                    <path fill-rule="evenodd"
                                        d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                                </svg>
                            </a>
                        </td>
                    </tr>
                   
                    </tbody>
                </table>
            </div>

            <!-- add button -->
            <div class="mb-3" style="margin-left: 35%;">
                <router-link to="/add_tracker" class="btn btn-outline-success btn-sm">
                    <!-- svg image for add -->
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-lg"
                        viewBox="0 0 16 16">
                        <path fill-rule="evenodd"
                            d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z"/>
                    </svg>
                    Add Tracker
                </router-link>
            </div>

        </div>

    </div>
    `,

    methods: {
        'delete_tracker': function (tid, index) {

            fetch(`http://127.0.0.1:5000/api/tracker/${tid}`, {
                    method: 'DELETE',
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.access_token}`
                    },
                }).then((response) => {
                    if (response.status == 401) {
                        this.$emit('sign_out', "something went wrong");
                    }
                    return response.json()
                }).then((data) => {
                    this.message = data.message;
                    this.trackers.splice(index,1);
                }).catch(error => { console.error("Error: ", error) }); 
        },

    },

    watch:{
        'trackers':function(){
            this.$forceUpdate();
        }
    },

    mounted: function () {
        if (!localStorage.access_token) {
            router.push({ path: '/login' })
            localStorage.clear();
        } else {
            if (this.trackers === "") {
                fetch(`http://127.0.0.1:5000/api/user/trackers`, {
                    method: 'GET',
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.access_token}`
                    },
                }).then((response) => {
                    if (response.status == 401) {
                        this.$emit('sign_out', "something went wrong");
                    }
                    if (response.status != 200) {
                        this.message = "Something went wrong."
                    }
                    return response.json()
                })
                    .then((data) => {
                        this.trackers = data;
                }).catch(error => { console.error("Error: ", error); });
            }
        }
    }

})


const AddTracker = Vue.component('AddTracker', {
    props: [],

    data: function () {
        return {
            uid: '',
            name: '',
            description: '',
            tracker_type: '',
            settings: ''
        }
    },

    template:
        `
    <div class="d-flex justify-content-center" style="margin-top:2%;">
    
        <div class="col-md-6" style="border:1px solid grey; padding: 2%;">
            <div>
                <h2>Add Tracker</h2>
                <br>
                
                <div class="mb-3">
                    <label for="tname" class="form-label">Name </label>
                    <input type="text" v-model="name" class="form-control" id="tname" name="tname" required>
                </div>

                <div class="mb-3">
                    <label for="desc" class="form-label">Description</label>
                    <textarea v-model="description"  class="form-control" id="desc" name="desc" ></textarea>
                </div>

                <div class="mb-3">
                    <label for="ttype" class="form-label">Tracker Type</label>
                    <select class="form-select" v-model="tracker_type" id="ttype" name="ttype" required>
                        <option>Numeric</option>
                        <option>Multiple Choice</option>
                        <option>Boolean</option>
                    </select>
                </div>

                <div class="mb-3">
                    <label for="settings" class="form-label">Settings</label>
                    <input type="text" v-model="settings" class="form-control" id="settings" name="settings">
                </div>

                    <input type="button" @click="add_tracker" class="btn btn-primary" value="Add">
                    <router-link to="/" class="btn btn-danger">Cancel</router-link>
                
            </div>
        </div>
    </div>

    `,

    methods: {
        'add_tracker': function () {
            this.message = "";

            fetch("http://127.0.0.1:5000/api/tracker", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.access_token}`
                },
                body: JSON.stringify({ "uid": localStorage.uid, "name": this.name, 
                                        "description": this.description, "tracker_type": this.tracker_type, "settings": this.settings })
            }).then((response) => {

                if (response.status == 401) {
                    this.$emit('sign_out', "something went wrong");
                }

                if (response.status == 201) {
                    console.log("successfully created tracker!!")
                }
                return response.json()
            })
                .then((data) => {
                    //console.log(data);
                    this.message = data.message;
                    router.push({ path: '/' })
                }).catch(error => { console.error("Error: ", error) });
        }
    }
})



const EditTracker = Vue.component('EditTracker', {
    props: ['id'],

    data: function () {
        return {
            tid:'',
            uid: '',
            name: '',
            description: '',
            tracker_type: '',
            settings: ''
        }
    },

    template:
        `
    <div class="d-flex justify-content-center" style="margin-top:2%;">
    
        <div class="col-md-6" style="border:1px solid grey; padding: 2%;">
            <div>
                <h2>Edit Tracker</h2>
                <br>
                
                <div class="mb-3">
                    <label for="tname" class="form-label">Name </label>
                    <input type="text" v-model="name" class="form-control" id="tname" name="tname" required>
                </div>

                <div class="mb-3">
                    <label for="desc" class="form-label">Description</label>
                    <textarea v-model="description"  class="form-control" id="desc" name="desc" ></textarea>
                </div>

                <div class="mb-3">
                    <label for="ttype" class="form-label">Tracker Type</label>
                    <select class="form-select" v-model="tracker_type" id="ttype" name="ttype" required>
                        <option>Numeric</option>
                        <option>Multiple Choice</option>
                        <option>Boolean</option>
                    </select>
                </div>

                <div class="mb-3">
                    <label for="settings" class="form-label">Settings</label>
                    <input type="text" v-model="settings" class="form-control" id="settings" name="settings">
                </div>

                    <input type="button" @click="edit_tracker" class="btn btn-primary" value="Add">
                    <router-link to="/" class="btn btn-danger">Cancel</router-link>
                
            </div>
        </div>
    </div>

    `,

    methods: {
        'edit_tracker': function () {
            this.message = "";

            fetch(`http://127.0.0.1:5000/api/tracker/${this.tid}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.access_token}`
                },
                body: JSON.stringify({ "uid": this.uid, "tid": this.tid, "name": this.name, 
                                        "description": this.description, "tracker_type": this.tracker_type, "settings": this.settings })
            }).then((response) => {

                if (response.status == 401) {
                    this.$emit('sign_out', "something went wrong");
                }

                if (response.status == 201) {
                    console.log("successfully created tracker!!")
                }
                return response.json()
            })
                .then((data) => {
                    //console.log(data);
                    this.message = data.message;
                    router.push({ path: '/' })
                }).catch(error => { console.error("Error: ", error) });
        }
    },

    mounted: function(){
        this.message = "";

            fetch(`http://127.0.0.1:5000/api/tracker/${this.id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.access_token}`
                },
            }).then((response) => {

                if (response.status == 401) {
                    this.$emit('sign_out', "something went wrong");
                }

                if (response.status == 200) {
                    console.log("Got the tracker!!");
                    this.message = "Got the tracker!";
                }
                return response.json()
            }).then((data) => {
                    
                this.tid = data.tid;
                this.uid = data.uid;
                this.name = data.name;
                this.description = data.description;
                this.tracker_type = data.tracker_type;
                this.settings = data.settings;
                    
            }).catch(error => { console.error("Error: ", error) });
    }
})


const TrackerDetail = Vue.component('TrackerDetail', {
    props : ['id'],

    data : function(){
        return {
            tracker:'',
            logs:'',
            message:'',
            logsX:[],
            logsY:[]

        }
    },

    template:
    `
    <div class="container" style="margin-top:2%;">

    <div class="text-center" style="margin-bottom: 1%;">
            <h2>{{ tracker.name }} - Tracker</h2>
        </div>

    <div class="row">

        <div class="col-md-6">
            <table class="table text-center">
                <thead>
                    <th>On</th>
                    <th>Value</th>
                    <th>Notes</th>
                    <th>Actions</th>
                </thead>
                <tbody>
                    
                    <tr v-for="(log, index) in logs">
                        <td>{{ log.log_time }}</td>
                        <td>{{ log.value }}</td>
                        <td>{{ log.notes }}</td>
                        <td>
                            <router-link :to="{path: '/tracker/' + log.tid + '/log/' + log.lid }"
                                class="link-success">
                                <!-- svg image for edit -->
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                    class="bi bi-pencil-square" viewBox="0 0 16 16">
                                    <path
                                        d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
                                    <path fill-rule="evenodd"
                                        d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z" />
                                </svg>
                            </router-link>
                            &nbsp; &nbsp;
                            <a href="#" @click="delete_log(log.lid, index)"
                                class="link-danger">
                                <!-- svg image for delete -->
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                    class="bi bi-trash" viewBox="0 0 16 16">
                                    <path
                                        d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" />
                                    <path fill-rule="evenodd"
                                        d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" />
                                </svg>
                            </a>
                        </td>
                    </tr>

                </tbody>
            </table>
            <router-link :to="{path: '/tracker/' + this.tracker.tid + '/log' }" class="btn btn-outline-success">Log</router-link>
            <router-link to="/" class="btn btn-outline-success">Go to Index</router-link>
        </div>

        <div class="col-md-6" id="plot" width="700px"height="400px">

         </div>
    </div>
</div>
    `,

    methods:{
        'delete_log': function(lid, index) {

            this.message = "";

            fetch(`http://127.0.0.1:5000/api/log/${lid}`, {
                    method: 'DELETE',
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.access_token}`
                    },
                }).then((response) => {
                    if (response.status == 401) {
                        this.$emit('sign_out', "something went wrong");
                    }
                    return response.json()
                }).then((data) => {
                    this.message = data.message;
                    this.logs.splice(index,1);
                }).catch(error => { console.error("Error: ", error) })

        }
    },

    mounted: function(){
        this.message = "";

            fetch(`http://127.0.0.1:5000/api/tracker/${this.id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.access_token}`
                },
            }).then((response) => {

                if (response.status == 401) {
                    this.$emit('sign_out', "something went wrong");
                }

                if (response.status == 200) {
                    console.log("Got the tracker!!");
                    //this.message = "Got the tracker!";
                }
                return response.json()
            }).then((data) => {
                    
                //console.log(data);
                this.tracker = data;
                     
            }).catch(error => { console.error("Error: ", error) });



            fetch(`http://127.0.0.1:5000/api/tracker/${this.id}/logs`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.access_token}`
                },
            }).then((response) => {

                if (response.status == 401) {
                    this.$emit('sign_out', "something went wrong");
                }

                if (response.status == 200) {
                    console.log("Got the tracker!!");
                }
                return response.json()
            }).then((data) => {
                    
                this.logs = data;

                for(l of this.logs){
                    this.logsX.push(l.log_time);
                    this.logsY.push(l.value);
                    }

                console.log(this.logsX, this.logsY);

                var myPlot = echarts.init(document.getElementById('plot'));

                var option = {
//                    title: {
//                        text: this.tracker.name + " Data"
//                    },

                    tooltip: {},

                    legend: {
                      data: ['values']
                    },

                    xAxis:{
                        data: this.logsX
                    },

                    yAxis: {

                    },

                    series: [
                      {
                        name: 'values',
                        type: ((this.tracker.tracker_type == "Numeric") ? 'line' : 'bar') ,
                        data: this.logsY
                      }
                    ]
                }

                myPlot.setOption(option);
                     
            }).catch(error => { console.error("Error: ", error) });

    }

})

const AddLog = Vue.component('AddLog', {
    props: ['id'],

    data: function(){
        return {
            tracker:'',
            log_value:'',
            notes:'',
            message:'',
            options:''
        }
    },

    template:
    `
    
    <div class="d-flex justify-content-center" style="margin-top:5%;">
    <div class="col-md-6" style="border:1px solid grey; padding: 2%;">
        <h2>Log - {{ tracker.name }}</h2>
        <br>
           
            <div class="mb-3" v-if="tracker.tracker_type == 'Numeric' ">
                <label class="form-label" for="tnumval">Tracker Value</label>
                <input type="text" v-model="log_value" class="form-control" name="tval" id="tnumval" required>
            </div>
           
            <div class="mb-3" v-if="tracker.tracker_type == 'Boolean' ">
                <label class="form-label">Tracker Value</label>
                <br>
                <input type="radio" v-model="log_value" class="form-check-input" id="y" name="tval" value="Yes">
                <label for="y" class="form-label">Yes</label><br>
                <input type="radio" v-model="log_value" class="form-check-input" id="n" name="tval" value="No">
                <label for="n" class="form-label">No</label><br>
            </div>
            
            <div class="mb-3" v-if="tracker.tracker_type == 'Multiple Choice' ">
                <label for="tchval" class="form-label">Tracker Value</label>
                <select id="tchval" v-model="log_value" class="form-select" name="tval" required>
                    <option v-for="op in this.options" :value="op">{{ op }}</option>
                </select>
            </div>
            
            <div class="mb-3">
                <label for="tnotes" class="form-label">Notes</label>
                <input type="text" v-model="notes" class="form-control" name="tnotes" id="tnotes">
            </div>

            <input @click="add_tracker_log" type="button" class="btn btn-primary" value="Log It">
            <router-link to="/" class="btn btn-danger">Cancel</router-link>
        </form>
    </div>
    </div>

    `,

    methods:{
        'add_tracker_log': function(){

            fetch(`http://127.0.0.1:5000/api/log`, {
                method: 'POST',

                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.access_token}`
                },
                body: JSON.stringify({ "tid": this.tracker.tid, "value": this.log_value, 
                                        "notes": this.notes  })
            }).then((response) => {

                if (response.status == 401) {
                    this.$emit('sign_out', "something went wrong");
                }

                if (response.status == 201) {
                    console.log("successfully created log!!")
                }
                return response.json()
            })
                .then((data) => {
                   // console.log(data);
                    //this.message = data.message;
                    router.push({ path: '/tracker/' + this.tracker.tid })
                }).catch(error => { console.error("Error: ", error) });

        }
    },

    mounted: function(){

        this.message = "";

        fetch(`http://127.0.0.1:5000/api/tracker/${this.id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.access_token}`
                },
            }).then((response) => {

                if (response.status == 401) {
                    this.$emit('sign_out', "something went wrong");
                }

                if (response.status == 200) {
                    console.log("Got the tracker!!");
                    //this.message = "Got the tracker!";
                }
                return response.json()
            }).then((data) => {
                    
                //console.log(data);
                this.tracker = data;

                if (data.tracker_type == "Multiple Choice"){
                    // this.options = data.settings.split(',')
                    let choices = data.settings.split(',');
                    let options = []
                    for (choice of choices){
                        options.push(choice.trim());
                    }

                    this.options = options;
                }
                     
            }).catch(error => { console.error("Error: ", error) });
    }
})


const EditLog = Vue.component('EditLog', {
    props: ['tid', 'id'],

    data: function(){
        return {
            log:'',
            tracker:'',
            log_value:'',
            notes:'',
            message:'',
            options:''
        }
    },

    template:
    `

    <div class="d-flex justify-content-center" style="margin-top:5%;">
    <div class="col-md-6" style="border:1px solid grey; padding: 2%;">
        <h2>Log - {{ tracker.name }}</h2>
        <br>

            <div class="mb-3" v-if="tracker.tracker_type == 'Numeric' ">
                <label class="form-label" for="tnumval">Tracker Value</label>
                <input type="text" v-model="log_value" class="form-control" name="tval" id="tnumval" required>
            </div>

            <div class="mb-3" v-if="tracker.tracker_type == 'Boolean' ">
                <label class="form-label">Tracker Value</label>
                <br>
                <input type="radio" v-model="log_value" class="form-check-input" id="y" name="tval" value="Yes">
                <label for="y" class="form-label">Yes</label><br>
                <input type="radio" v-model="log_value" class="form-check-input" id="n" name="tval" value="No">
                <label for="n" class="form-label">No</label><br>
            </div>

            <div class="mb-3" v-if="tracker.tracker_type == 'Multiple Choice' ">
                <label for="tchval" class="form-label">Tracker Value</label>
                <select id="tchval" v-model="log_value" class="form-select" name="tval" required>
                    <option v-for="op in this.options" :value="op">{{ op }}</option>
                </select>
            </div>

            <div class="mb-3">
                <label for="tnotes" class="form-label">Notes</label>
                <input type="text" v-model="notes" class="form-control" name="tnotes" id="tnotes">
            </div>

            <input @click="edit_tracker_log" type="button" class="btn btn-primary" value="Log It">
            <router-link to="/" class="btn btn-danger">Cancel</router-link>
        </form>
    </div>
    </div>

    `,

    methods:{
        'edit_tracker_log': function(){

            fetch(`http://127.0.0.1:5000/api/log/${this.log.lid}`, {
                method: 'PUT',

                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.access_token}`
                },
                body: JSON.stringify({ "tid": this.tracker.tid, "value": this.log_value,
                                        "notes": this.notes  })
            }).then((response) => {

                if (response.status == 401) {
                    this.$emit('sign_out', "something went wrong");
                }

                if (response.status == 201) {
                    console.log("successfully created log!!")
                }
                return response.json()
            })
                .then((data) => {
                    console.log(data);
                    //this.message = data.message;
                    router.push({ path: '/tracker/' + this.tracker.tid })
                }).catch(error => { console.error("Error: ", error) });

        }
    },

    mounted: function(){

        this.message = "";

        fetch(`http://127.0.0.1:5000/api/tracker/${this.tid}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.access_token}`
                },
            }).then((response) => {

                if (response.status == 401) {
                    this.$emit('sign_out', "something went wrong");
                }

                if (response.status == 200) {
                    console.log("Got the tracker!!");
                }
                return response.json()
            }).then((data) => {

                console.log(data);
                this.tracker = data;

                if (data.tracker_type == "Multiple Choice"){
                    this.options = data.settings.split(',')
                }

            }).catch(error => { console.error("Error: ", error) });



            fetch(`http://127.0.0.1:5000/api/log/${this.id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.access_token}`
                },
            }).then((response) => {

                if (response.status == 401) {
                    this.$emit('sign_out', "something went wrong");
                }

                if (response.status == 200) {
                    console.log("Got the log!!");
                }
                return response.json()
            }).then((data) => {

                console.log(data);
                this.log = data;

                this.log_value = this.log.value;
                this.notes = this.log.notes;

            }).catch(error => { console.error("Error: ", error) });
    }
})



const routes = [
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/', component: Index, props: true },
    { path: '/add_tracker', component: AddTracker, props: true },
    { path: '/edit_tracker/:id', component: EditTracker, props: true },
    { path: '/tracker/:id', component: TrackerDetail, props: true },
    { path: '/tracker/:id/log', component: AddLog, props: true },
    { path: '/tracker/:tid/log/:id', component: EditLog, props: true },
]


const router = new VueRouter({
    routes // short for `routes: routes`
})



let app = new Vue({
    el: '#app',

    router: router,

    data: {
        fname: localStorage.fname,
        access_token: localStorage.access_token,
        uid: localStorage.uid,
        message: ''
    },

    methods: {
        'sign_out': function (message="") {
            localStorage.clear();
            this.fname = '';
            this.access_token = '';
            //this.message = message;
            this.$forceUpdate();
            router.push({ path: '/login' })
        },

        'set_data': function () {
            console.log("Set the data!")
            this.access_token = localStorage.access_token;
            this.fname = localStorage.fname;
            this.uid = localStorage.uid;
        },

        'set_message': function(msg){
            this.message = msg;
        }
    },

    computed: {

    },

    mounted: function () {
        this.message = "";
    }
})