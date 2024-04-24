describe('R8UC1', () => {

  let uid
  let name
  let email
  let tid
  
  before(function() {
    cy.fixture('test_user.json').then((user) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
      }).then((response) => {
        cy.wait(5000)
        uid = response.body._id.$oid
        name = user.firstName + ' ' + user.lastName
        email = user.email
        //expect(response.body._id.$oid).to.eq(uid)
      })
    })
    
    // cy.fixture('test_task.json').then((task) => {
    //   cy.request({
    //     method: 'POST',
    //     url: `http://localhost:5000/tasks/create`,
    //     form: true,
    //     body: task
    //   }).then((response) => {
    //     tid = response.body._id.$oid
    //   })
    // })

      // let task = {
      //   "title": "talk to IT",
      //   "description": "hello",
      //   "url": "U_gANjtv28g",
      //   "userid": uid
      // }

    cy.request({
      method: 'POST',
      url: `http://localhost:5000/tasks/create`,
      form: true,
      body: {
        title: "talk to IT",
        description: "hello",
        url: "U_gANjtv28g",
        todos: [
            "Watch video", 
            "Evaluate usability of tools", 
            "Check out BundlePhobia and investigate npm packages in most recent projects"
        ],
        userid: uid
      }
    })

  })
  




    beforeEach(function () {
      // enter the main main page
      cy.visit('http://localhost:3000')
    })
  
    it('starting out on the landing screen', () => {
      // make sure the landing page contains a header with "login"
      cy.get('h1')
        .should('contain.text', 'Login')
    })
  
    it('login to the system with an existing account', () => {
      // detect a div which contains "Email Address", find the input and type (in a declarative way)
      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type(email)
      // alternative, imperative way of detecting that input field
      //cy.get('.inputwrapper #email')
      //    .type(email)
  
      // submit the form on this page
      cy.get('form')
        .submit()
  
      // assert that the user is now logged in
      cy.get('h1')
        .should('contain.text', 'Your tasks, ' + name)
    })

    
  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})
