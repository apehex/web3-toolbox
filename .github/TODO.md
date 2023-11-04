## Parsing

[ ] parse ALL trace types into the SAME output

## Performances

[ ] RPC load balancer = new RPC endpoint

## Indexing

[ ] transparent indexing:
    [ ] use Parquet files / DB
[ ] scrape Zettablock?
[ ] use cryo to cache all the data?
[ ] collect evidence:
    [ ] => address, bytecode, deployer, tx, labels, etc upon detection

## Testing

[ ] test on cryo data
[ ] pickle dataset:
    [ ] metamorphic tx
    [ ] meta traces
    [ ] random traces & transactions
[ ] modules:
    [x] alerts
    [ ] findings
    [ ] indexing
    [x] logging
    [ ] parsing:
        [x] address
        [ ] metadata
        [x] traces
        [x] event logs
        [x] transactions
    [ ] profiling
    [ ] scraping
