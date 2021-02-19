var vm = new Vue({
   el: '#app',
   vuetify: new Vuetify({}),
   delimiters: ['${', '}'],
   data: {
      idEmployee: "",
      listEmployees: [],
      headers: [
         { text: 'ID', value: 'id' },
         { text: 'Name', value: 'name' },
         { text: 'Contract Type Name', value: 'contractTypeName' },
         { text: 'Role ID', value: 'roleId' },
         { text: 'Role Name', value: 'roleName' },
         { text: 'Role Description', value: 'roleDescription' },
         { text: 'Hourly Salary', value: 'hourlySalary' },
         { text: 'Monthly Salary', value: 'monthlySalary' },
         { text: 'Anual Salary', value: 'anualSalary' },
       ],
       snackbar: false,
   },
   methods: {
      getData: function () {
         var me = this;
         me.listEmployees = [];
         const URL = `http://0.0.0.0:8000/api/employees/${me.idEmployee}`;
         axios.get(URL, {'responseType': 'json'})
            .then(function (res) {
               if (res.status == 200) {
                  const data = res.data;
                  if (Array.isArray(data)){
                     me.listEmployees = res.data;
                  }else{
                     me.listEmployees = [res.data];
                  }
               }
            })
            .catch(function (err) {
               me.snackbar = true;
            });
      }
   }
})