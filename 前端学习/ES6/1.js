// const p = new Promise(function (resolve, reject) {
//   throw new Error('test');
// })

// p.catch(function (error) {
//   console.error(error);
// })

// // Error: test


const someAsyncThing = function () {
  return new Promise(function (resolve, reject) {
    resolve(x + 1)
  })
}

const someOtherAsyncThing = function () {
  return new Promise(function (resolve, reject) {
    resolve(x + 2)
  })
}

someAsyncThing().then(function () {
  return someOtherAsyncThing()
}).catch(function (error) {
  console.log('Error1: ', error)
  y + 1;
}).catch(function (error) {
  console.log('carry on:', error)
})