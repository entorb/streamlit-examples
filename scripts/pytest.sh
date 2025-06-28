#!/bin/sh
cd $(dirname $0)/..

pytest --cov --cov-report=html:coverage_report
