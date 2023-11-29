## Package

[x] remove web3 from production, keep as dev dependency
[ ] specify typings
[ ] document the functionalities

## Parsing

[ ] parse ALL trace types into the SAME output
[ ] all parsing function return the identity on themselves

## Performances

[ ] RPC load balancer = new RPC endpoint

## Indexing

[ ] transparent indexing:
    [x] use Parquet files / DB
        [x] compatible with cryo
        [ ] import / export several datasetS at once (instead of just contracts)
        [ ] split module: IO + schemas + query + casting
    [ ] Zettablock?
[ ] use cryo to cache all the data?
[ ] collect evidence:
    [ ] => address, bytecode, deployer, tx, labels, etc upon detection

## Testing

[ ] test on cryo data
[x] pickle dataset:
    [x] metamorphic tx
    [x] meta traces
    [x] random traces & transactions
[ ] modules:
    [x] alerts
    [x] findings
    [ ] indexing
        [ ] pickle
        [ ] parquet
        [ ] zettablock
    [x] logging
    [x] parsing:
        [x] address
        [x] metadata
        [x] traces
        [x] event logs
        [x] transactions
    [ ] profiling
    [ ] scraping
