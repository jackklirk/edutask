describe('R8UC1', () => {
  let uid
  let name
  let email
  
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
            todos: 'Watch',
            userid: uid
          }
        })
      })
    })
  })
  
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
    cy.get('div.title-overlay')
      .should('contain.text', 'talk to IT')
  })
      
  it('ID 1 - opening the task', () => {
    cy.contains('div.title-overlay', 'talk to IT')
    .click()

    cy.get('p span.editable')
    .should('contain.text', 'hello')

    cy.get('h1 span.editable')
    .should('contain.text', 'talk')
  })

  it('ID 2 - Add empty todo item', () =>{
    cy.contains('div.title-overlay', 'talk to IT')
    .click()
    cy.get('form.inline-form').find('input[type=submit]').click()
    cy.get('li.todo-item').should('have.length', 1)
  })

  it('ID 3 - Add a todo item with description', () =>{
    cy.contains('div.title-overlay', 'talk to IT')
    .click()
    cy.get('form.inline-form').find('input[type=text]').type('Ask why fans speed up')
    cy.get('form.inline-form').find('input[type=submit]').click()
    cy.contains('li.todo-item', 'Ask why fans speed up')
  })

    after(function () {
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${uid}`
      }).then((response) => {
        cy.log(response.body)
      })    
    })
  
  })

describe('R8UC2', () => { 
  let uid
  let name
  let email

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
            todos: "Watch",
            userid: uid
          }
        })
      })
    })
  })

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
      cy.contains('div.title-overlay', 'talk to IT')
      .click()
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

  it('ID 1 - Mark todo as done', () => {
    

    cy.get('span.checker.unchecked')
    .click()

    cy.get('span.checker.checked').should('exist')

  })

  it('ID 2 - Unmark todo', () => {
    

    cy.get('span.checker.checked')
    .click()

    cy.get('span.checker.unchecked').should('exist')

  })

  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    })
  })
})

describe('R8UC3', () => { 
  let uid
  let name
  let email

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
        cy.request({
          method: 'POST',
          url: `http://localhost:5000/tasks/create`,
          form: true,
          body: {
            title: "talk to IT",  
            description: "hello",
            url: "U_gANjtv28g",
            todos: "Watch",
            userid: uid
          }
        })
      })
    })
  })

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
      cy.contains('div.title-overlay', 'talk to IT')
      .click()
    })

  it('ID 1 - deleting existing todo', () => {
    cy.get('span.remover')
    .click().then(cy.get('li.todo-item').should('not.exist'))
  })

  after(function () {
    // clean up by deleting the user from the database 
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    })
  })
})
