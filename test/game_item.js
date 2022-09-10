const GameItem = artifacts.require("GameItem");

/*
 * uncomment accounts to access the test accounts made available by the
 * Ethereum client
 * See docs: https://www.trufflesuite.com/docs/truffle/testing/writing-tests-in-javascript
 */
contract("GameItem", function (/* accounts */) {
  it("should assert true", async function () {
    await GameItem.deployed();
    return assert.isTrue(true);
  });
});
