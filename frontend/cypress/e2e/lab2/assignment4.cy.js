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
        uid = response.body._id.$oid
        name = user.firstName + ' ' + user.lastName
        email = user.email
        // then() works async, it runs just after the previous statment
        // looks like the request must be in the "then()" to the id to be defined
        // https://docs.cypress.io/guides/core-concepts/variables-and-aliases#Closures
        cy.request({
          method: 'POST',
          url: `http://localhost:5000/tasks/create`,
          form: true,
          body: {
            title: "talk to IT",
            description: "hello",
            url: "U_gANjtv28g",
            // This was also the problem, if we send a list(like it is in the dummy) it crashes *facepalm*
            // todos: [
            //   "Watch video", 
            //   "Evaluate usability of tools", 
            //   "Check out BundlePhobia and investigate npm packages in most recent projects"
            // ],
            todos: "watch video",
            userid: uid
          }
        }).then((response) => {
          //tid = response[0].body._id.$oid
          // After thinking for a while I am not sure if we really need the task id
          tid = response.body[0]._id.$oid
        })
      })
    })
  })
  // RESPONSE OF THE TASK CREATION ON POSTMAN
  //   [
  //     {
  //         "_id": {
  //             "$oid": "66298c883016dc0f54698142"
  //         },
  //         "categories": [],
  //         "description": "\"How to tie a tie\"",
  //         "startdate": {
  //             "$date": "2024-04-25T00:49:44.366Z"
  //         },
  //         "title": "\"Tie a tie\"",
  //         "todos": [
  //             {
  //                 "_id": {
  //                     "$oid": "66298c883016dc0f54698141"
  //                 },
  //                 "description": "\"watch video\"",
  //                 "done": false
  //             }
  //         ],
  //         "video": {
  //             "_id": {
  //                 "$oid": "66298c883016dc0f54698140"
  //             },
  //             "url": "\"U_dasjndjank\""
  //         }
  //     }
  // ]
    
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
  
    beforeEach(function () {
      // enter the main main page
      cy.visit('http://localhost:3000')
      cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)
      cy.get('form')
      .submit()
      cy.get('h1')
      .should('contain.text', 'Your tasks, ' + name)
    })
    
    
    it('checking if the task exists', () =>{
      // a hint here is to have the application on the browser and inspect the desired
      // elements with the right click
      cy.get('div.title-overlay')
        .should('contain.text', 'talk to IT')
    })
      
    it('opening the task', () => {
      cy.get('img[src="http://i3.ytimg.com/vi/U_gANjtv28g/hqdefault.jpg"]')
      .click()

      cy.get('p span.editable')
      .should('contain.text', 'hello')

      cy.get('h1 span.editable')
      .should('contain.text', 'talk')

      cy.get('li.todo-item')
      .should('contain.text', 'watch')
    })

    // beforeEach(function () {
    //   // enter the main main page
    //   cy.visit('http://localhost:3000')
    //   cy.contains('div', 'Email Address')
    //   .find('input[type=text]')
    //   .type(email)
    //   cy.get('form')
    //   .submit()
    //   cy.contains('div.title-overlay', 'talk to IT')
    //   //cy.get('img')
    //   .click()
    // })
       
    it('toggle existing todo', () => {
      cy.get('img[src="http://i3.ytimg.com/vi/U_gANjtv28g/hqdefault.jpg"]')
      .click()

      cy.get('span.checker.unchecked')
      .click()

      cy.get('span.checker.checked').should('exist')

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
